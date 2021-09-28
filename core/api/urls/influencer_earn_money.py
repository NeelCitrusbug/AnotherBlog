from django.urls import  path
from core.api.views.influencer_earned_money import (
    InfluencerEarnMoneyListAPIView,
)

urlpatterns = [
    path("", InfluencerEarnMoneyListAPIView.as_view(), name="influencer-eran-money-list"),
]
