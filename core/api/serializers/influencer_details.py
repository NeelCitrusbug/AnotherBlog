from rest_framework import serializers

from core.models import User, UserProfile, InfluencerOffer, Event
from core.api.serializers import UserUpdateDetailsSerializer, CategorySerializer, EventListSerializer, InfluencerOfferListSerializer

from django.utils import timezone

now = timezone.now()

# -----------------------------------------------------------------------------
# Banners serializers
# -----------------------------------------------------------------------------


class InfluencerDetailsListSerializer(serializers.ModelSerializer):
    
    user = UserUpdateDetailsSerializer()
    influencer = CategorySerializer()
    offer = serializers.SerializerMethodField('get_offers')
    upcoming_events = serializers.SerializerMethodField('get_upcoming_events')
    similar_events = serializers.SerializerMethodField('get_similar_events')

    
    """
    Serializes the Banner data into JSON
    """

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "influencer",
            "photo",
            "video",
            "about",
            "offer",
            "upcoming_events",
            "similar_events",

        )

    def get_offers(self, user_object):
        request = self.context.get('request')
        offer = InfluencerOffer.objects.filter(user__id=user_object.user.id)
        serializers = InfluencerOfferListSerializer(offer, many=True, context={"request": request})
        return serializers.data



    def get_upcoming_events(self, user_object):

        request = self.context.get('request')
        event = Event.objects.filter(user__id=user_object.user.id, event_date_time__gte=now, active=True).order_by("event_date_time")
        serializers = EventListSerializer(event, many=True, context={"request": request})
        return serializers.data


    def get_similar_events(self, user_object):
        request = self.context.get('request')
        event = Event.objects.filter(event_date_time__gte=now, active=True).order_by("event_date_time")[:2]
        serializers = EventListSerializer(event, many=True, context={"request": request})
        return serializers.data
