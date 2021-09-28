from rest_framework import serializers

from core.models import User
# -----------------------------------------------------------------------------
# User serializers
# -----------------------------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    """Serializes the User data into JSON"""

    class Meta:
        model = User
        fields = ["id","username", "email",]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


# -----------------------------------------------------------------------------
# My forked version
# -----------------------------------------------------------------------------


class MyUserSerializer(serializers.ModelSerializer):
    
    """
    Serializes the User data into JSON
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "name",
            "email",
            "influencer_stripe_account_id",
           
        )
        
        
        