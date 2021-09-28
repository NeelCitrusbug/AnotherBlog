from rest_framework import serializers

from core.models import Category

# -----------------------------------------------------------------------------
# Credit/ Debit Card serializers
# -----------------------------------------------------------------------------

class CategorySerializer(serializers.ModelSerializer):
    
    """
    Serializes the Card data into JSON
    """

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
           
        )