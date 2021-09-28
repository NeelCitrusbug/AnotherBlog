from rest_framework import serializers

from core.models import Credit

# -----------------------------------------------------------------------------
# Credit serializers
# -----------------------------------------------------------------------------


class CreditSerializer(serializers.ModelSerializer):
    
    """
    Serializes the Credit data into JSON
    """

    class Meta:
        model = Credit
        fields = (
            "id",
            "price",
            "number_of_credit", 
        )

