# -*- coding: utf-8 -*-

from django.urls import  path
from rest_framework.routers import DefaultRouter

from core.api import views
 
urlpatterns = [
    path('facebook', views.FacebookLogin.as_view(), name='fb_login'),
    path('twitter', views.TwitterLogin.as_view(), name='twitter_login'),
    path('github', views.GithubLogin.as_view(), name='github_login'),
]
 