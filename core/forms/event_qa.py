from django import forms
from core.models import EventPracticeAudienceQA

# -----------------------------------------------------------------------------
# Event Practice Audience QA
# -----------------------------------------------------------------------------

class EventPracticeAudienceQAForm(forms.ModelForm):

    """Custom Banner Form"""

    class Meta():
        model = EventPracticeAudienceQA
        fields = [
            "event",
            'question',
            "answer",
            ]


    def __init__(self, *args, **kwargs):

        super(EventPracticeAudienceQAForm, self).__init__(*args, **kwargs)

        self.fields['event'].required = True
        self.fields['question'].required = True
        self.fields['answer'].required = True