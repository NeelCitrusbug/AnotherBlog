from rest_framework import serializers

from core.models import Card
from core.utils import MyStripe

# -----------------------------------------------------------------------------
# Credit/ Debit Card serializers
# -----------------------------------------------------------------------------


class CardSerializer(serializers.ModelSerializer):
    
    """
    Serializes the Card data into JSON
    """

    class Meta:
        model = Card
        fields = (
            "id",
            "user",
            "stripe_card_id",
            "last4",
            "card_expiration_date",
            'created_at',
        
        )


class CardListSerializer(serializers.ModelSerializer):
    card_expiration_date = serializers.SerializerMethodField('get_card_expiration_date')
    
    """
    Serializes the Card data into JSON
    """

    class Meta:
        model = Card
        fields = (
            "id",
            "user",
            "stripe_card_id",
            "last4",
            "card_expiration_date",
            'created_at',
        
        )

    def get_card_expiration_date(self, card):
        card = card.card_expiration_date.split("/")
        if int(card[0]) <9:
            new_format = "0{0}/{1}".format(card[0], card[1][2:4])
            return new_format
        else:
            new_format = "{0}/{1}".format(card[0], card[1][2:4])
            return new_format