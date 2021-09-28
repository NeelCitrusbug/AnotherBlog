from rest_framework import serializers

from core.models import Transactionlog

# -----------------------------------------------------------------------------
# from core.models import Transactionlog log serializers
# -----------------------------------------------------------------------------


class TransactionlogSerializer(serializers.ModelSerializer):
    
    """
    Serializer the Transaction log data into JSON
    """

    class Meta:
        
        model = Transactionlog

        fields = (
            "id",
            "user",
            "transaction_type",
            "amount",
            "credit",
            "types",
            "transaction_status" ,   
            "transaction_id",           
        )

