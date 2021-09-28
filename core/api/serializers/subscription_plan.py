from rest_framework import serializers

from core.models import SubscriptionPlan

# -----------------------------------------------------------------------------
# from core.models import Subscription Plan serializers
# -----------------------------------------------------------------------------


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    
    """
    Serializes the Subscription Plan data into JSON
    """

    class Meta:
        model = SubscriptionPlan

        fields = (
            "id",
            "title",
            "price",
            "number_of_credit",
            "description",
           
        )
