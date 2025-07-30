from django.urls import path
from .views import post_list, post_detail, edit_comment, delete_comment

from . import views

app_name='blog'

urlpatterns=[
    path('',views.post_list,name='post_list'),
    path('<int:pk>/',views.post_detail,name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('comment/<int:comment_id>/edit',views.edit_comment,name='edit_comment'),
    path('comment/<int:comment_id>/delete',views.delete_comment,name='delete_comment'),
    path('upload/',views.upload_image,name='upload_image'),
    path('gallery/', views.image_gallery, name='image_gallery'),
    path('gallery/<int:id>/', views.image_detail, name='image_detail'),
    path('gallery/<int:id>/delete/', views.image_delete, name='image_delete'),

]