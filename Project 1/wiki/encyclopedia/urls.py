from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="wiki_entry"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("edit/", views.edit, name="edit"),
    path("submit/", views.submit_edit, name="submit"),
    path("random/", views.random_entry, name="random")
]
