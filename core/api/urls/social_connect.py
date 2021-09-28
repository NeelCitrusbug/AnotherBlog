# -*- coding: utf-8 -*-

from django.urls import  path
from rest_framework.routers import DefaultRouter

from core.api import views
 
urlpatterns = [
    path('facebook', views.FacebookConnect.as_view(), name='fb_connect'),
    path('twitter', views.TwitterConnect.as_view(), name='twitter_connect'),
    path('github', views.GithubConnect.as_view(), name='github_connect'),
]
  