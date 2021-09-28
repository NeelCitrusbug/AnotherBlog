from django import forms
from core.models import Faq

# -----------------------------------------------------------------------------
# Faq
# -----------------------------------------------------------------------------

class FaqForm(forms.ModelForm):

    """Custom Banner Form"""

    class Meta():
        model = Faq
        fields = [
            "faq_types",
            'question',
            "answer",
            ]


    def __init__(self, *args, **kwargs):

        super(FaqForm, self).__init__(*args, **kwargs)

        self.fields['faq_types'].required = True
        self.fields['question'].required = True
        self.fields['answer'].required = True

