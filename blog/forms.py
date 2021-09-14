from django import forms
from .models import Post,Category
from django_select2 import forms as s2forms




class CategoryWidget(s2forms.ModelSelect2MultipleWidget):
    model = Category
    search_fields = [
        'name__icontains',
        
    ]



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author','created_date','published_date']
        # fields = (
        #     "title",
        #     "category",
        #     "text",
        # )

    

        widgets = {
            
            "category":CategoryWidget,
            "title": forms.TextInput(attrs={'placeholder': 'Enter Title Here'}),
            "text" : forms.Textarea(
                attrs={'placeholder': 'Enter description here'}),
        }

    
    





