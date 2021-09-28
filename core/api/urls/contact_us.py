from django.urls import  path
from core.api.views.contact_us import (
    ContactUsCreateAPI,

)

urlpatterns = [

    path("", ContactUsCreateAPI.as_view(), name="contact-us"),
]
