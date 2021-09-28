from rest_framework import serializers

from core.models import Category

# -----------------------------------------------------------------------------
# InfluencerCategory Serializer 
# -----------------------------------------------------------------------------


class InfluencerCategorySerializer(serializers.ModelSerializer):
    
    """
    Serializes the Banner data into JSON
    """

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )
 