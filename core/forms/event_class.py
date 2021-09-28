from django import forms
from core.models import EventClass

# -----------------------------------------------------------------------------
# Event Class
# -----------------------------------------------------------------------------


class EventClassForm(forms.ModelForm):

    """Custom Banner Form"""

    class Meta():
        model = EventClass
        fields = [
            "user",
            "name",
            "description",
            "active",
            ]


    def __init__(self, *args, **kwargs):

        super(EventClassForm, self).__init__(*args, **kwargs)

        self.fields['user'].required = True
        self.fields['name'].required = True
        self.fields['description'].required = True

