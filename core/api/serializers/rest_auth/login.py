from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.db.models import Q
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from core.utils import CustomValidation
from core.models import TokenModel, User, UserProfile
from core.utils import import_callable

from django.core import serializers as coreserializers

from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from sorl.thumbnail import get_thumbnail

from django.contrib.sites.models import Site

from core.api.serializers.subscription_plan import SubscriptionPlanSerializer
from django.contrib.auth.models import Group

from .reset_password import PasswordResetForm



# Get the UserModel
UserModel = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'}, required=False, allow_blank=True)
    raise_exception = False

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise CustomValidation(msg, status_code=status.HTTP_200_OK)

        return user

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise CustomValidation(msg, status_code=status.HTTP_200_OK)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise CustomValidation(msg, status_code=status.HTTP_200_OK)

        return user

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        # oc = Otp.objects.filter(user_id=user, status=True).count()
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise CustomValidation(msg, status_code=status.HTTP_200_OK)
            else:
                ob = UserModel.objects.get(email__iexact=email)
                if "firebase_token" in attrs:
                    ob.firebase_token = attrs.get("firebase_token")
                    print("TOKEN UPDATED")  # get firebase token from request & update in user object

                if "device_type" in attrs:
                    ob.device_type = attrs.get("device_type")

                ob.save()
        else:
            check_email = User.objects.filter(email=email).exists()
            check_active = User.objects.filter(email=email, is_active=False).exists()
            if not check_email:
                msg = _('Email does not exist.')
            elif check_active:
                msg = _('User account is disabled.')
            else:
                msg = _('The password you entered is incorrect')
    
            raise CustomValidation(msg, status_code=status.HTTP_200_OK)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    msg = _('E-mail is not verified.')
                    raise CustomValidation(msg, status_code=status.HTTP_200_OK)

        attrs['user'] = user
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    class Meta:
        model = TokenModel
        fields = ('key',)


class UserGroupSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('name',)

    def get_name(self, obj):
        return obj.name



class UserDetailsSerializer(serializers.ModelSerializer):

    first_name = serializers.SerializerMethodField('get_first_name')

    """
    User model w/o password
    """

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'is_active',
            "is_influencer",
            "influencer_stripe_account_id",
            'first_name',

        )

        read_only_fields = ('email', 'user_permissions', 'first_name')


    def get_first_name(self, user):

        if user.name:
            name = str(user.name).split(" ")
            return name[0]

        else:
            return user.name     



class ProfileDetailsSerializer(serializers.ModelSerializer):

    subscription = SubscriptionPlanSerializer()
    user = UserDetailsSerializer()


    class Meta:
        model = UserProfile
        fields = (
            'id',
            'user',
            'subscription',
            'photo',
            'video',
            'about',
            'credit',
            'follower',
            'is_popular',
            'stripe_subscription_id',
        )



class JwtSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        """
        Required to allow using custom USER_DETAILS_SERIALIZER in
        JWTSerializer. Defining it here to avoid circular imports
        """

        user_data = UserDetailsSerializer(obj['user'], context=self.context).data

        return user_data


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            # raise serializers.ValidationError(self.reset_form.errors)
            raise CustomValidation(self.reset_form.errors, status_code=status.HTTP_200_OK)

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        opts.update(self.get_email_options())

        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    
    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            # raise ValidationError({'uid': ['Invalid value']})
            raise CustomValidation({'uid': ['Invalid value']}, status_code=status.HTTP_200_OK)


        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            # raise ValidationError({'token': ['Invalid value']})
            raise CustomValidation({'token': ['Invalid value']}, status_code=status.HTTP_200_OK)

        return attrs

    def save(self):
        return self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', False
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            # raise serializers.ValidationError('Invalid password')
            msg = 'Invalid password'
            raise CustomValidation(msg, status_code=status.HTTP_200_OK)

        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            # raise serializers.ValidationError(self.set_password_form.errors)
            raise CustomValidation(self.set_password_form.errors, status_code=status.HTTP_200_OK)

        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)


class UserUpdateDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = (
            'id',
            'name',
            'email',
            "influencer_stripe_account_id",
        )

        read_only_fields = ('email', 'user_permissions', 'password','influencer_stripe_account_id')
