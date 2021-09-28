from django.urls import  path
from core.api.views.influencer_category import (
    CategoryListAPIView,

)

urlpatterns = [

    path("", CategoryListAPIView.as_view(), name="credit-list"),
]
