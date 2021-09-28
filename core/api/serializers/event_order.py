from rest_framework import serializers

from core.models import EventOrder, UserProfile
from .event import EventListSerializer

# -----------------------------------------------------------------------------
# EventOrder serializers
# -----------------------------------------------------------------------------


class EventOrderSerializer(serializers.ModelSerializer):
    
    """
    Serializes the EventOrder data into JSON
    """

    class Meta:
        model = EventOrder
        fields = (
            "id",
            "user",
            "event", 
            "used_credit", 
            "created_at", 
            "charge_id", 
            'order_status',

        )



class EventOrderListSerializer(serializers.ModelSerializer):
    event=EventListSerializer()
    influencer_category = serializers.SerializerMethodField('get_influencer_category')
    
    """
    Serializes the EventOrder data into JSON
    """

    class Meta:
        model = EventOrder
        fields = (
            "id",
            "user",
            "event", 
            "used_credit", 
            "created_at", 
            "charge_id", 
            'order_status',
            'influencer_category'

        )

    def get_influencer_category(self, event):
        user=UserProfile.objects.filter(user__id=event.user.id).first()
        if user.influencer:
            return user.influencer.name
        else:
            return ''    