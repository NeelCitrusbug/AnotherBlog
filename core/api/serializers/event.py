from rest_framework import serializers

from core.models import Event, Agenda, UserProfile, InfluencerOffer
from .event_class import EventClassSerializer
from core.api.serializers import UserUpdateDetailsSerializer, InfluencerOfferListSerializer
from core.api.serializers.agenda import AgendaSerializer

import datetime, pytz

# -----------------------------------------------------------------------------
# Event serializers
# -----------------------------------------------------------------------------


class EventSerializer(serializers.ModelSerializer):
    
    """
    Serializes the Event data into JSON
    """

    class Meta:
        model = Event
        fields = (
            "id",
            "user",
            "about",
            "event_types",
            "event_class",
            "event_date_time",
            "price",
            "photo",
            "number_of_participants",
            "credit_required",
            "session_lenght",
            "time_zone",

        
        )



class EventListSerializer(serializers.ModelSerializer):
    event_class = EventClassSerializer()
    user = UserUpdateDetailsSerializer()
    remaining_spots = serializers.SerializerMethodField('get_remaining_spots')
    influencer_category = serializers.SerializerMethodField('get_influencer_category')
    agenda = serializers.SerializerMethodField('get_agenda')
    event_offer = serializers.SerializerMethodField('get_event_offer')


    
    """
    Serializes the Event data into JSON
    """

    class Meta:
        model = Event
        fields = (
            "id",
            "user",
            "about",
            "event_types",
            "event_class",
            "event_date_time",
            "price",
            "photo",
            "number_of_participants",
            "credit_required",
            "session_lenght",
            "is_featured",
            "is_popular",
            "created_at",
            "remaining_spots",
            "time_zone",
            "agenda",
            "influencer_category",
            'event_offer',

        
        )

    def get_remaining_spots(self, event):
        if event.number_of_participants>=event.remianing_spots:
            remaining_spots = int(event.number_of_participants) - int(event.remianing_spots)
            return remaining_spots
        else:
            return 0


    def get_influencer_category(self, event):

        user=UserProfile.objects.filter(user__id=event.user.id).first()
        if user.influencer:
            return user.influencer.name
        else:
            return ''    

    
    def get_agenda(self, user_object):

        request = self.context.get('request')
        event = Agenda.objects.filter(event__id=user_object.id)
        serializers = AgendaSerializer(event, many=True, context={"request": request})
        return serializers.data
        

     
    def get_event_offer(self, event):

        request = self.context.get('request')
        event = InfluencerOffer.objects.filter(event__id=event.id)
        serializers = InfluencerOfferListSerializer(event, many=True, context={"request": request})
        return serializers.data    

        