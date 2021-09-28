from rest_framework import serializers

from core.models import SubscriptionOrder
from .subscription_plan import SubscriptionPlanSerializer

# -----------------------------------------------------------------------------
# from core.models import Subscription Order serializers
# -----------------------------------------------------------------------------


class SubscriptionOrderSerializer(serializers.ModelSerializer):
    subscription=SubscriptionPlanSerializer()
    
    """
    Serializes the Subscription Order data into JSON
    """

    class Meta:
        
        model = SubscriptionOrder

        fields = (
            "id",
            "user",
            "subscription",
            "amount",
            "charge_id",
            "ordre_status",
            "stripe_subscription_id",
            "plan_status",
            "expire_date" ,
            "created_at",          
        )
