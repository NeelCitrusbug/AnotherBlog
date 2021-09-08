from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



# class Category(models.Model):

#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse("post_list")