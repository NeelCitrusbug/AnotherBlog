from rest_framework import serializers

from core.models import InfluencerOffer, Offer

# -----------------------------------------------------------------------------
# Credit/ Debit Card serializers
# -----------------------------------------------------------------------------

class OfferSerializer(serializers.ModelSerializer):
    
    """
    Serializes the Card data into JSON
    """

    class Meta:
        model = Offer
        fields = (
            "id",
            "title",
            "description",
            'icon',
            'created_at'
         
        
        )


class InfluencerOfferListSerializer(serializers.ModelSerializer):
    offer =OfferSerializer()
    
    """
    Serializes the Card data into JSON
    """

    class Meta:
        model = InfluencerOffer
        fields = (
            "id",
            "user",
            "offer",
         
        
        )

class InfluencerOfferSerializer(serializers.ModelSerializer):
    
    """
    Serializes the Card data into JSON
    """

    class Meta:
        model = InfluencerOffer
        fields = (
            "id",
            "user",
            "offer",
            "event"
         
        
        )
