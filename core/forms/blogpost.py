from django import forms
from blog.models import Post
# -----------------------------------------------------------------------------
# Blogpost
# -----------------------------------------------------------------------------


class BlogpostForm(forms.ModelForm):

    """Custom Blogpost Form"""

    class Meta():
        model = Post
        fields = [
            "author",
            "title",
            "category",
            "text",
            "created_date",
            "published_date",
            ]


    def __init__(self, *args, **kwargs):

        super(BlogpostForm, self).__init__(*args, **kwargs)

        self.fields['author'].required = True
        self.fields['title'].required = True
        self.fields['category'].required = True
        self.fields['text'].required = True
        self.fields['created_date'].required = True
        


