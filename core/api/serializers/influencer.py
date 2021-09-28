from rest_framework import serializers

from core.models import User, UserProfile
from core.api.serializers import UserUpdateDetailsSerializer
from .influencer_category import InfluencerCategorySerializer

# -----------------------------------------------------------------------------
# Banners serializers
# -----------------------------------------------------------------------------


class InfluencerListSerializer(serializers.ModelSerializer):
    
    user = UserUpdateDetailsSerializer()
    influencer = InfluencerCategorySerializer()
    
    """
    Serializes the Banner data into JSON
    """

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "influencer",
            "photo",
            "video",
            "about",
            "follower",
            "is_popular",
        )


