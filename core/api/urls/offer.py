from django.urls import  path
from core.api.views.offer import (
    InfluencerOfferAPIView ,
    InfluencerOfferCreateAPI,

)

urlpatterns = [

    path("", InfluencerOfferAPIView.as_view(), name="offer-list"),
    path("add/", InfluencerOfferCreateAPI.as_view(), name="offer-create"),
]
