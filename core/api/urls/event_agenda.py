from django.urls import  path
from core.api.views.event_agenda import (
    EventAgendaAPIView,
    EventAgendaCreateAPI,
    EventAgendaUpdateAPI,
    EventAgendaDeleteAPI,


)

urlpatterns = [

    path("<int:pk>", EventAgendaAPIView.as_view(), name="event-agenda-list"),
    path("create/", EventAgendaCreateAPI.as_view(), name="event-agenda-create"),
    path('update/<int:pk>', EventAgendaUpdateAPI.as_view(), name='event-agenda-update"'), 
    path('delete/<int:pk>', EventAgendaDeleteAPI.as_view(), name='event-agenda-delete"'), 
]
