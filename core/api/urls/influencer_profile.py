from django.urls import  path
from core.api.views.influencer_profile import (
    InfluencerProfileDetailsView,
    InfluencerProfileUpdateView,

)

urlpatterns = [

    path("", InfluencerProfileDetailsView.as_view(), name="influencer-details"),
    path("update/", InfluencerProfileUpdateView.as_view(), name="influencer-details-update"),

]
