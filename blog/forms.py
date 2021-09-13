from django import forms
from .models import Post,Category
from django_select2 import forms as s2forms


# choices = Category.objects.all().values_list("name", "name")
# print(choices)

# choice_list = []

# for item in choices:
#     choice_list.append(item)

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

    
        # widgets = {
        #     "category": forms.SelectMultiple(attrs={"class": "form-control", "name":"name[]", "multiple":"multiple"}),
           
        # }

        widgets = {
            # "category":CategoryWidget(attrs={'class':'form-control'}),
            "category":CategoryWidget,
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class' : 'form-control custom-select select2-selection'})
        
    # category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),widget=forms.SelectMultiple(attrs={"class": "form-control"}), choices = choice_list)

        # widgets = {
        #     "category": CategoryWidget,
            
        # }


# , "name":"states[]", "multiple":"multiple"


