from rest_framework import serializers
from .subscription_plan import SubscriptionPlanSerializer


from core.models import UserProfile
# -----------------------------------------------------------------------------
# User serializers
# -----------------------------------------------------------------------------

class UserProfileSerializer(serializers.ModelSerializer):

    subscription=SubscriptionPlanSerializer()
    """Serializes the User data into JSON"""

    class Meta:
        model = UserProfile
        fields = ["id","user", "subscription", "credit", "stripe_subscription_id"]


