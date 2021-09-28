from django import forms
from core.models import Agenda

# -----------------------------------------------------------------------------
# Agenda
# -----------------------------------------------------------------------------

class AgendaForm(forms.ModelForm):

    """Custom Agenda Form"""

    class Meta():
        model = Agenda
        fields = [
            "event",
            'title',
            "description",
            ]

    def __init__(self, *args, **kwargs):

        super(AgendaForm, self).__init__(*args, **kwargs)

        self.fields['event'].required = True
        self.fields['title'].required = True
