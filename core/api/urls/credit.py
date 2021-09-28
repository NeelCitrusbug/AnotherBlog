from django.urls import  path
from core.api.views.credit import (
    CreditListAPIView,
    CreditPurchaseAPI,

)

urlpatterns = [

    path("", CreditListAPIView.as_view(), name="credit-list"),
    path("add-credit/", CreditPurchaseAPI.as_view(), name="add-credit"),
]
