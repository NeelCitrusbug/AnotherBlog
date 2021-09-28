from django import forms
from core.models import Credit

# -----------------------------------------------------------------------------
# Credit
# -----------------------------------------------------------------------------


class CreditForm(forms.ModelForm):

    """ Custom Credit Form"""

    class Meta():
        model = Credit
        fields = [
            "price",
            "number_of_credit",
            ]

        required = [
            "price",
            "number_of_credit",
            ]   
  
    def __init__(self, *args, **kwargs):

        super(CreditForm, self).__init__(*args, **kwargs)
        
        self.fields['price'].required = True
        self.fields['number_of_credit'].required = True
