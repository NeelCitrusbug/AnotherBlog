from django import forms
from core.models import Banner

# -----------------------------------------------------------------------------
# Banner
# -----------------------------------------------------------------------------


class BannerForm(forms.ModelForm):

    """Custom Banner Form"""

    class Meta():
        model = Banner
        fields = [
            "title",
            "image",
            "description",
            ]

        labels  = {
                "image": "Image Size: 730px x 623px"
         }



    def __init__(self, *args, **kwargs):

        super(BannerForm, self).__init__(*args, **kwargs)

        self.fields['title'].required = True
        self.fields['image'].required = True
        self.fields['description'].required = True


