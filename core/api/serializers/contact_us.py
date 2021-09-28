from rest_framework import serializers

from core.models import ContactUs

# -----------------------------------------------------------------------------
# ContactUs serializers
# -----------------------------------------------------------------------------


class ContactUsSerializer(serializers.ModelSerializer):
    
    """
    Serializes the ContactUs data into JSON
    """

    class Meta:
        model = ContactUs
        fields = (
            "id",
            "email",
        )


