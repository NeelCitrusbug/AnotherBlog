
import unicodedata

from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
from core.utils import Emails, send_sendgrid_email
from django.conf import settings

import datetime

from rest_framework import serializers

UserModel = get_user_model()


class UserDetailsSerializer(serializers.ModelSerializer):

    first_name = serializers.SerializerMethodField('get_first_name')
    """
    User model w/o password
    """

    class Meta:
        model = UserModel
        fields = (
            'id',
            'name',
            'email',
            'is_active',
            "is_influencer",
            'first_name'
        )

        read_only_fields = ('email', 'user_permissions','first_name')


    def get_first_name(self, user):

        if user.name:
            name = str(user.name).split(" ")
            return name[0]

        else:
            return user.name    
       

def _unicode_ci_compare(s1, s2):
    
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()


class PasswordResetForm(forms.Form):

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
       
        serializer=UserDetailsSerializer(context['user'])
        current_date = str(datetime.datetime.now())
        date_time_obj =datetime.datetime.strptime(current_date, '%Y-%m-%d %H:%M:%S.%f')

        context['user']= serializer.data
        context['date']= date_time_obj.strftime("%d %B, %Y")
        context['time']= date_time_obj.strftime("%H:%M %p")

        send_sendgrid_email(context,"Reset Password",to_email, settings.PASSWORD_RESET_TEMPLATE_ID)



    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password() and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )