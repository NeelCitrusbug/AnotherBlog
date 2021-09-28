from django import forms
from core.models import UserProfile

# -----------------------------------------------------------------------------
# UserProfile
# -----------------------------------------------------------------------------

class UserProfileForm(forms.ModelForm):
    
    """ Custom UserProfile Form"""

    class Meta():
        model = UserProfile
        fields = ["user","influencer", "follower", "is_popular", "photo", "about"]
