from django import forms
from core.models import SubscriptionPlan

# -----------------------------------------------------------------------------
# SubscriptionPlan
# -----------------------------------------------------------------------------


class SubscriptionPlanForm(forms.ModelForm):

    """Custom SubscriptionPlan Form"""

    class Meta():
        model = SubscriptionPlan
        fields = [
            "title",
            "price",
            "number_of_credit",
            "description",
            ]

        required = [
            "title",
            "price",
            "number_of_credit",
            ]       

    def __init__(self, *args, **kwargs):

        super(SubscriptionPlanForm, self).__init__(*args, **kwargs)
       
        self.fields['title'].required = True
        self.fields['price'].required = True
        self.fields['number_of_credit'].required = True