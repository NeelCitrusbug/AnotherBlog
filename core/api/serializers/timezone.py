from rest_framework import serializers


# -----------------------------------------------------------------------------
# Timezone serializers
# -----------------------------------------------------------------------------


class TimezoneSerializer(serializers.Serializer):
    timezone = serializers.CharField()
    
   