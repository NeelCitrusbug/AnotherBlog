from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name", unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="author")
    title = models.CharField(max_length=200, verbose_name="title")
    category = models.ManyToManyField(Category,verbose_name="categories")
    text = models.TextField(verbose_name="description")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="date when post created")
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="date when post published")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):  
        return self.title



