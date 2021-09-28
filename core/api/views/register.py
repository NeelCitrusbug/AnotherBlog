from rest_auth.registration.views import RegisterView
from django.conf import settings
from allauth.account import app_settings as allauth_settings
from rest_auth.app_settings import (TokenSerializer,
                                    JWTSerializer,
                                    create_token)
                                    
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from core.api.serializers import RegisterSerializer
from rest_auth.utils import jwt_encode
from allauth.account.utils import complete_signup
from core.models import User, UserProfile
from core.utils import modify_api_response


class MyRegisterView(RegisterView):
    
    serializer_class = RegisterSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        response = modify_api_response(response)
        return super().finalize_response(request, response, *args, **kwargs)

    def get_response_data(self, user, request):

        user = User.objects.get(pk=user.pk)
        
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent.")}
            
        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                    'user': user,
                    'token': self.token
            }
            return JWTSerializer(data,context={'request':request}).data
        else:
            return TokenSerializer(user.auth_token).data

    def create(self, request, *args, **kwargs):
         
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({"status": "OK", "message": "Account created successfully.You will receive a link in email to login in your account", "data": self.get_response_data(user, request)})


    def perform_create(self, serializer):

        user = serializer.save(self.request)
        UserProfile.objects.create(user=user)
 
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(user)
        else:
            create_token(self.token_model, user, serializer)

        complete_signup(self.request._request, user,
                        allauth_settings.EMAIL_VERIFICATION,
                        None)
       
        return user