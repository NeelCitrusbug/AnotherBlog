from django.urls import  path
from core.api.views.billing_details import (
    CardAPIView,
    CardCreateAPI,

)

urlpatterns = [

    path("", CardAPIView.as_view(), name="card-list"),
    path("add/", CardCreateAPI.as_view(), name="card-create"),
]
