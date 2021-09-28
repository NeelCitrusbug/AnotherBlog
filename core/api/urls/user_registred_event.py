from django.urls import path
from core.api.views.user_registred_event import (
    UserEventRegisteredAPIView,

)

urlpatterns = [

    path("", UserEventRegisteredAPIView.as_view(), name="user-registered-event"),
]
