from rest_framework import serializers

from core.models import CreditOrder
from .credit import CreditSerializer

# -----------------------------------------------------------------------------
# CreditOrder serializers
# -----------------------------------------------------------------------------


class CreditOrderSerializer(serializers.ModelSerializer):
    
    """
    Serializes the CreditOrder data into JSON
    """

    class Meta:
        model = CreditOrder
        fields = (
            "id",
            "user",
            "credit", 
            "amount", 
            "created_at", 
            "charge_id", 
            'order_status',

        )



class CreditOrderListSerializer(serializers.ModelSerializer):
    credit=CreditSerializer()
    
    """
    Serializes the CreditOrder data into JSON
    """

    class Meta:
        model = CreditOrder
        fields = (
            "id",
            "user",
            "credit", 
            "amount", 
            "created_at", 
            "charge_id", 
            'order_status',

        )