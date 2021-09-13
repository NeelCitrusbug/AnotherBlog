from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=100, verbose_name="Category Name", unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.ManyToManyField(Category,verbose_name="categories")
    text = models.TextField(verbose_name="description")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="date when post created")
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="date when post published")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_category_values(self):
        ret = ''
        print(self.category.all())
        # use models.ManyToMany field's all() method to return all the Category objects that this post belongs to.
        for cats in self.category.all():
            ret = ret + cats.name + ','
        # remove the last ',' and return the value.
        return ret[:-1]

    def __str__(self):  
        return self.title



# class Category(models.Model):

#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse("post_list")