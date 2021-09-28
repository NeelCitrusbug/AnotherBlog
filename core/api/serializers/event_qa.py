from rest_framework import serializers

from core.models import EventPracticeAudienceQA

# -----------------------------------------------------------------------------
# Event Practice Audience QA serializers
# -----------------------------------------------------------------------------


class EventPracticeAudienceQASerializer(serializers.ModelSerializer):
    
    """
    Serializes the Event Practice Audience QA data into JSON
    """

    class Meta:
        model = EventPracticeAudienceQA
        fields = (
            "id",
            "event",
            "question", 
            "answer", 
        
        )

