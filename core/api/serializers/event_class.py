from rest_framework import serializers

from core.models import EventClass

# -----------------------------------------------------------------------------
# Event Class serializers
# -----------------------------------------------------------------------------


class EventClassSerializer(serializers.ModelSerializer):
    
    """
    Serializes the EventClass data into JSON
    """

    class Meta:
        model = EventClass
        fields = (
            "id",
            "user",
            "name",
            "description",
        )

