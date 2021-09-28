from django.urls import  path
from core.api.views.script import (
    ScriptCreateAPI,
    ScriptListAPIView,
    ScriptUpdateAPI,
    ScriptDeleteAPI,

)

urlpatterns = [

    path("<int:pk>", ScriptListAPIView.as_view(), name="script-class-list"),
    path("create/", ScriptCreateAPI.as_view(), name="script-class-create"),
    path('update/<int:pk>', ScriptUpdateAPI.as_view(), name='script-class-update"'), 
    path('delete/<int:pk>', ScriptDeleteAPI.as_view(), name='script-class-delete"'), 

]
