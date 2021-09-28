from rest_framework import serializers

from core.models import InfluencerTransferredMoney

# -----------------------------------------------------------------------------
# Influencer Transferred Money serializers
# -----------------------------------------------------------------------------


class InfluencerTransferredMoneySerializer(serializers.ModelSerializer):
    
    """
    Serializes the Banner data into JSON
    """

    class Meta:
        model = InfluencerTransferredMoney
        fields = ["id", 'user','transfer_amount', 'status', "transaction_id", "created_at","total_amount","kuzo_amount"]
     