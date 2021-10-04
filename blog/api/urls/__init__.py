from django.urls import include, path
from . import blogpost



urlpatterns = [
    path('post/',include(blogpost)),
]