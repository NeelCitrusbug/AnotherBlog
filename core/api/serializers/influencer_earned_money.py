from rest_framework import serializers

from core.models import User, UserProfile, InfluencerOffer, Event, EventOrder
from core.api.serializers import UserUpdateDetailsSerializer, CategorySerializer, EventListSerializer, InfluencerOfferListSerializer

from django.utils import timezone
from django.db.models import Sum


now = timezone.now()

# -----------------------------------------------------------------------------
# Banners serializers
# -----------------------------------------------------------------------------


class InfluencerEarnMoneySerializer(serializers.ModelSerializer):

    total_earned_amount = serializers.SerializerMethodField('get_total_earn_amount')


    
    """
    Serializes the Banner data into JSON
    """

    class Meta:
        model = EventOrder
        fields = (
            "id",
            "total_earned_amount",
       
        )

    def get_total_earn_amount(self, obj):
        print(obj)

        return 0



   




