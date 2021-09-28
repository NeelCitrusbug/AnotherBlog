from django.urls import  path
from core.api.views.event_qa import (
    EventPracticeAudienceQAAPIView,
    EventPracticeAudienceQACreateAPI,
    EventPracticeAudienceQAUpdateAPI,
    EventPracticeAudienceQADeleteAPI,


)

urlpatterns = [

    path("<int:pk>", EventPracticeAudienceQAAPIView.as_view(), name="event-qa-list"),
    path("create/", EventPracticeAudienceQACreateAPI.as_view(), name="event-qa-create"),
    path('update/<int:pk>', EventPracticeAudienceQAUpdateAPI.as_view(), name='event-qa-update"'), 
    path('delete/<int:pk>', EventPracticeAudienceQADeleteAPI.as_view(), name='event-qa-delete"'), 
]
