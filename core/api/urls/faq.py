from django.urls import  path
from core.api.views.faq import (
    FaqListAPIView,

)

urlpatterns = [

    path("", FaqListAPIView.as_view(), name="faq-list"),
]
