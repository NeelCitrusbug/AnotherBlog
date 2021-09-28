from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_auth.app_settings import (
    TokenSerializer, UserDetailsSerializer, LoginSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer,
    PasswordChangeSerializer, JWTSerializer, create_token
)
from rest_auth.models import TokenModel
from rest_auth.utils import jwt_encode
from core.utils import Emails
from core.api.apiviews import MyGenericAPIView, MyAPIView
sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


from allauth.account.views import ConfirmEmailView
from rest_auth.registration.serializers import VerifyEmailSerializer

from core.models import User
from core.utils import modify_api_response
from django.contrib.auth.hashers import check_password



class LoginView(MyGenericAPIView):

    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel


    def finalize_response(self, request, response, *args, **kwargs):
        # Override response (is there a better way to do this?)
        response = modify_api_response(response)
        return super().finalize_response(request, response, *args, **kwargs)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):
            response_serializer = JWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data['user']

        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})


        
        response = Response({"status": "OK", "message": "Login successful", "data": serializer.data})


        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                from datetime import datetime
                expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
                                    self.token,
                                    expires=expiration,
                                    httponly=True)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        
        self.serializer.is_valid(raise_exception=True)
         
        self.login()
        return self.get_response()


class LogoutView(MyAPIView):

    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        if getattr(settings, 'ACCOUNT_LOGOUT_ON_GET', False):
            response = self.logout(request)
        else:
            response = self.http_method_not_allowed(request, *args, **kwargs)

        return self.finalize_response(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response({"status": "OK", "message": "Successfully logged out.", "data": []})
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)
        return response


class PasswordResetView(MyGenericAPIView):

    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = User.objects.filter(email__iexact=request.data["email"])

            if user.exists():
        
                # Return the success message with OK HTTP status
                return Response({"status": "OK", "message": "Password reset e-mail has been sent.", "data": []})
            else:
                return Response({"status": "FAIL", "message": "No user found with this email.", "data": []})
        else:
            return Response({"status": "FAIL", "message": "Something went wrong, please try again!", "data": serializer.errors})


class PasswordResetConfirmView(MyGenericAPIView):

    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "OK", "message": "Password has been reset with the new password.", "data": []})
        else:
            return Response(
                {"status": "FAIL", "message": "Something is wrong with the password.", "data": serializer.errors})


class PasswordChangeView(MyGenericAPIView):
    
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "OK", "message": "New password has been saved.", "data": []})
        else:
            return Response({"status": "FAIL", "message": "Something is wrong with the password.", "data": serializer.errors})


class ChangeCurrentPassword(MyAPIView):

    def put(self, request):


        if request.user.is_authenticated:

            try:
                user = User.objects.get(pk=request.user.id)

                current_password = request.data['current_password']
                new_password1= request.data['new_password']
                new_password2= request.data['confirm_password']

                check_user_password = check_password(current_password, user.password)

                if not check_user_password:
                    return Response({"status": "FAIL", "message": "The current password you entered is incorrect", "data": []})

                if new_password1!=new_password2:
                    return Response({"status": "FAIL", "message": "The new password you entered does not match", "data": []})


                user.set_password(new_password1)
                user.save()
                return Response({"status": "OK", "message": "Successfully changed password.", "data": {"id":user.id}})


            except User.DoesNotExist:
                    return Response({"status": "FAIL", "message": "user not found", "data": []})

        else:
            return Response({"status": "FAIL", "message": "user not found", "data": []})


# Email verification

class VerifyEmailView(APIView, ConfirmEmailView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):

        from rest_framework_jwt.settings import api_settings

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']

        confirmation = self.get_object()
        confirmation.confirm(self.request)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(confirmation.email_address.user)
        token = jwt_encode_handler(payload)

        return Response({'detail': _('ok'), 'token':token}, status=status.HTTP_200_OK)


