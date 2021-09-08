from django import forms
from .models import Post


# choices = Category.objects.all().values_list("name", "name")
# print(choices)

# choice_list = []

# for item in choices:
#     choice_list.append(item)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "text",
        )

        # widgets = {
        #     "category": forms.Select(
        #         choices=choice_list, attrs={"class": "form-control"}
        #     ),
        # }
