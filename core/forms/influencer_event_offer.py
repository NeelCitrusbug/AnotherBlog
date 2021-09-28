from django import forms
from core.models import InfluencerOffer

# -----------------------------------------------------------------------------
# InfluencerOffer
# -----------------------------------------------------------------------------

class InfluencerOfferForm(forms.ModelForm):

    """Custom InfluencerOffer Form"""

    class Meta():
        model = InfluencerOffer
        fields = [
            "user",
            "offer",
            ]
    def __init__(self, *args, **kwargs):
        super(InfluencerOfferForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = True
        self.fields['offer'].required = True
