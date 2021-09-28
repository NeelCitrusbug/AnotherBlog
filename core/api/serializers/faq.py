from rest_framework import serializers

from core.models import Faq

# -----------------------------------------------------------------------------
# Faq serializers
# -----------------------------------------------------------------------------


class FaqSerializer(serializers.ModelSerializer):
    
    """
    Serializes the Faq data into JSON
    """

    class Meta:
        model = Faq
        fields = (
            "id",
            "faq_types",
            "question", 
            "answer", 

        )
