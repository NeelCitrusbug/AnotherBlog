from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from core.utils import CustomValidation
try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

from rest_framework import serializers

from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from allauth.account.utils import send_email_confirmation
from allauth.account.admin import EmailAddress
from core.models import User

# -----------------------------------------------------------------------------
# Register serializer
# -----------------------------------------------------------------------------




@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True

    user.save()


class RegisterSerializer(serializers.Serializer):
    

    name = serializers.CharField()
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password = serializers.CharField(write_only=True)


    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)

        user=User.objects.filter(email=email).first()
        user_obj =EmailAddress.objects.filter(user=user, verified=False).exists()

        if user_obj:
            user.delete()
        
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                msg = _("A user is already registered with this e-mail address.")
                raise CustomValidation(msg, status_code=status.HTTP_200_OK)

        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)


    def custom_signup(self, request, user):

        pass

    def get_cleaned_data(self):
        
        return {
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            'name': self.validated_data.get('name', ''),
        }

    def save(self, request):

        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


