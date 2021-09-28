from rest_framework import serializers

from core.models import Agenda

# -----------------------------------------------------------------------------
# Agenda serializers
# -----------------------------------------------------------------------------


class EventAgendaSerializer(serializers.ModelSerializer):
    
    """
    Serializes the Agenda data into JSON
    """

    class Meta:
        model = Agenda
        fields = (
            "id",
            "event",
            "title",
            "description",
        
        )

