# -*- coding: utf-8 -*-

from django.urls import path
from rest_framework.routers import DefaultRouter

from core.api import views 

urlpatterns = [
    path('<int:pk>', views.GithubLogin.as_view(), name='uert'), 
    
]
 