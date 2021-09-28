from rest_framework import serializers

from core.models.evnt_script import EventScript

# -----------------------------------------------------------------------------
# EventScript serializers
# -----------------------------------------------------------------------------


class EventScriptSerializer(serializers.ModelSerializer):
    
    """
    Serializes the EventScript data into JSON
    """

    class Meta:
        model = EventScript
        fields = (
            "id",
            "event",
            "title"

        )
