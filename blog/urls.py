from django.urls import path,include
from . import views

app_name = 'blog'

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/new/", views.create_post, name="post_new"),
    path("post/<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("post/<pk>/publish/", views.post_publish, name="post_publish"),
    path("post/<pk>/remove", views.post_remove, name="post_remove"),
    path("drafts/", views.post_draft_list, name="post_draft_list"),
    path("category/", views.CategoryList.as_view(), name= "category_list"),
    path("category/new", views.CategoryNew.as_view(), name="category_new"),
    path('category/<category>', views.CategoryPostList.as_view(), name= "category_post_list"),
    path('category/<category>/remove', views.category_remove, name= "category_remove"),
    path('category/<pk>/edit',views.CategoryUpdateView.as_view(), name="category_edit"),


    path('blogpost-list/', views.blogpost_list),
    path('blogpost-detail/<int:pk>/', views.blogpost_detail),

   ]



