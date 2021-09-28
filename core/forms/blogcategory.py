from django import forms
from blog.models import Category

# -----------------------------------------------------------------------------
# Blogpost
# -----------------------------------------------------------------------------


class BlogcategoryForm(forms.ModelForm):

    """Custom Blogpost Form"""

    class Meta():
        model = Category
        fields = [
            
            "name",
            ]


    def __init__(self, *args, **kwargs):

        super(BlogcategoryForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = True
        


