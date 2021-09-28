from django import forms
from core.models import Category

# -----------------------------------------------------------------------------
# Category
# -----------------------------------------------------------------------------


class CategoryForm(forms.ModelForm):

    """Custom Category Form"""

    class Meta():
        model = Category
        fields = [
            "name",
            ]

    def __init__(self, *args, **kwargs):

        super(CategoryForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = True
 