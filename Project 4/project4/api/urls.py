from django.urls import path

from . import views

urlpatterns = [
    path('posts/new/', views.create_new_post, name='new_post'),
    path('posts/all/', views.get_all_posts, name='get_all_posts'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/unlike/', views.unlike_post, name='unlike_post'),
    path('users/<int:user_id>/', views.get_user_profile, name='get_user'),
]