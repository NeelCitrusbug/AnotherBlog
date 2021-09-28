from django import forms
from .models import Post,Category
from django_select2 import forms as s2forms

# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CategoryWidget(s2forms.ModelSelect2MultipleWidget):
    model = Category
    search_fields = [
        'name__icontains',
        
    ]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author','created_date','published_date']
        
        widgets = {
            
            "category":CategoryWidget,
            "title": forms.TextInput(attrs={'type':'text','class':"form-control",'placeholder': 'Enter Title Here'}),
            "text" : forms.Textarea(
                attrs={'class':"form-control",'placeholder': 'Enter description here'}),
        }

    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)

        widgets = {
            "name":forms.TextInput(attrs={'type':'text','class':"form-control",'placeholder': 'Enter Category Here'}),
        }




# # -----------------------------------------------------------------------------
# # Users
# # -----------------------------------------------------------------------------

# class MyUserCreationForm(UserCreationForm):

#     """
#     Custom UserCreationForm.
#     """

#     class Meta(UserCreationForm.Meta):
#         model = get_user_model()
#         fields = [
#             "password1",
#             "is_active",
#             "email",
#             "name",
#             'is_influencer',
#         ]

#     def __init__(self, user, *args, **kwargs):
#         # self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)
#         self.user = user
#         self.fields['name'].required = True

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.username=instance.email
#         instance.save()
#         if commit:
#             instance.save()
#         return instance


# class MyUserChangeForm(UserChangeForm):
#     """
#     Custom UserChangeForm.
#     """

#     class Meta(UserChangeForm.Meta):
#         model = get_user_model()
#         fields = [
#             "is_active",
#             "email",
#             "name",
#             'is_influencer',
#         ]

#     def __init__(self, user, *args, **kwargs):
#         # self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)
#         self.user = user




# # -----------------------------------------------------------------------------
# # UserProfile
# # -----------------------------------------------------------------------------

# class UserProfileForm(forms.ModelForm):
    
#     """ Custom UserProfile Form"""

#     class Meta():
#         model = UserProfile
#         fields = ["user","influencer", "follower", "is_popular", "photo", "about"]