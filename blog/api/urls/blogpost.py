from django.urls import path,include
from .. import views


urlpatterns = [
    #django rest framwork urlpatterns starts here
    
    path('list/', views.BlogpostList.as_view()),
    path('create/', views.BlogpostCreate.as_view()),
    path('detail/<int:pk>/', views.BlogpostDetail.as_view()),
    path('update/<int:pk>/', views.BlogpostUpdate.as_view()),
    path('delete/<int:pk>/', views.BlogpostDelete.as_view()),
    

   ]
