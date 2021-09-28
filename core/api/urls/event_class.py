from django.urls import  path
from core.api.views.event_class import (
    EventClassAPIView,
    EventClassCreateAPI,
    EventClassUpdateAPI,
    EventClassDeleteAPI,

)

urlpatterns = [

    path("", EventClassAPIView.as_view(), name="event-class-list"),
    path("create/", EventClassCreateAPI.as_view(), name="event-class-create"),
    path('update/<int:pk>', EventClassUpdateAPI.as_view(), name='event-class-update"'), 
    path('delete/<int:pk>', EventClassDeleteAPI.as_view(), name='event-class-delete"'), 

]
