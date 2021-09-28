# -*- coding: utf-8 -*-
from django.urls import include, path
from .. import views
from django.views.generic import TemplateView
from . import urls_auth, views,  urls_core



urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="index"), 
    path("", include(urls_auth)),
    path("", include(urls_core)),

    # User management 
    path("accounts/", include("allauth.urls")),

]
