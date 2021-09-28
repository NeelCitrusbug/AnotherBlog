from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest
from django.contrib.auth.models import Group
from allauth.account.adapter import app_settings
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from core.utils import CustomValidation, validate_password
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from core.utils import Emails, send_sendgrid_email


class AccountAdapter(DefaultAccountAdapter):


    def send_confirmation_mail(self, request, emailconfirmation, signup):

        activate_url = settings.FRONTEND_URL+"/verify-link/{0}".format(emailconfirmation.key)
        first_name=''
        if emailconfirmation.email_address.user:
            name = str(emailconfirmation.email_address.user).split(" ")
            first_name+=name[0]

        else:
            first_name+=emailconfirmation.email_address.user


        ctx = {
            "user": str(emailconfirmation.email_address.user),
            'first_name':first_name,
            "activate_url": str(activate_url),
            "subject":"Welcome !!!",
        }
        send_sendgrid_email(ctx, "Welcome !!!", emailconfirmation.email_address.email, settings.EMAIL_VERIFICATION_TEMPLATE_ID)
        return 


    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def clean_name(self, name):
        return name

    def clean_password(self, password, user=None):
        """
        Validates a password. You can hook into this if you want to
        restric the allowed password choices.
        """
        min_length = app_settings.PASSWORD_MIN_LENGTH
        if min_length and len(password) < min_length:
            msg = _("Password must be a minimum of {0} characters.").format(min_length)
            # raise forms.ValidationError(_("Password must be a minimum of {0} "
            #                               "characters.").format(min_length))
            raise CustomValidation(msg, status_code=status.HTTP_200_OK)

        validate_password(password, user)
        return password
        
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_username, user_email, user_field
 
        data = form.cleaned_data
        email = data.get('email')
        user_email(user, email)
    

        name = data.get('name')
        if name:
            user_field(user, 'name', name)


        if 'password' in data:
            user.set_password(data["password"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
 

        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()

            # group = Group.objects.get(name=user_type)
            # user.groups.add(group)

        return user

        


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

