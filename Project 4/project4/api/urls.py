from django.urls import path

from . import views

urlpatterns = [
    path('posts/new/', views.new_post, name='new_post'),
]
