from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create_listing"),
    path("<int:listing_id>/", views.listing, name="listing"),
    path("<int:listing_id>/comments/", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/remove/<int:listing_id>/", views.watchlist_remove, name="watchlist_remove"),
    path("watchlist/add/<int:listing_id>/", views.watchlist_add, name="watchlist_add"),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:category_id>/", views.get_category, name="get_category"),
    path("<int:listing_id>/close/", views.close_listing, name="close_listing"),
]
