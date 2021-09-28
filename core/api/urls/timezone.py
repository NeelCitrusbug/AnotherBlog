from django.urls import  path
from core.api.views.timezone import (
    TimezoneListAPIView,

)

urlpatterns = [

    path("", TimezoneListAPIView.as_view(), name="timezone-list"),
]

