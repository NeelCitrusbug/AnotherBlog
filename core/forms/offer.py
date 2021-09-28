from django import forms
from core.models import Offer

# -----------------------------------------------------------------------------
# Offer
# -----------------------------------------------------------------------------

class OfferForm(forms.ModelForm):

    """Custom Offer Form"""
    class Meta():
        model = Offer
        fields = [
            "title",
            "icon",
            "description",
            ]

        labels  = {
                "icon": "Icon Size: 50px x 50px"
         }

    def __init__(self, *args, **kwargs):

        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['icon'].required = True
        self.fields['description'].required = True
