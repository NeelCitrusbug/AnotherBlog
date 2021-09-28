from django.urls import  path
from core.api.views.subscribe_plan import (
    SubscriptionPlanListAPIView,    
)

urlpatterns = [

    path("", SubscriptionPlanListAPIView.as_view(), name="subscribe-plan-list"),

]
