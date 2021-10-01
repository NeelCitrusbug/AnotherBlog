from django.db import models
from django.conf import settings
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name", unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

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

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):  
        return self.title



