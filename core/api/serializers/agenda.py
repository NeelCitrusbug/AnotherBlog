from rest_framework import serializers

from core.models import Agenda

# -----------------------------------------------------------------------------
# Agenda serializers
# -----------------------------------------------------------------------------


class AgendaSerializer(serializers.ModelSerializer):
    
    """
    Serializes the Banner data into JSON
    """

    class Meta:
        model = Agenda
        fields = (
            "id",
            "event",
            "title",
            "description",
        )
 