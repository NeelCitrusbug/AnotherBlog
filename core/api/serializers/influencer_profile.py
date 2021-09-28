from rest_framework import serializers
from core.api.serializers.rest_auth.login import UserUpdateDetailsSerializer
from core.models import UserProfile
from .influencer_category import InfluencerCategorySerializer

# -----------------------------------------------------------------------------
# Influencer profile serializers
# -----------------------------------------------------------------------------


class InflunecerUserProfileSerializer(serializers.ModelSerializer):
    influencer = InfluencerCategorySerializer()
    user = UserUpdateDetailsSerializer()

    """Serializes the User data into JSON"""

    class Meta:
        model = UserProfile
        fields = ["id", "user", "influencer", "photo", "video", "about"]


class InflunecerUserProfileUpdateSerializer(serializers.ModelSerializer):

    """Serializes the User data into JSON"""

    class Meta:
        model = UserProfile
        fields = ["id", "user", "influencer", "photo", "video", "about"]
