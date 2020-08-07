
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("create-post", views.create_post, name="create_post"),
    path("posts", views.posts, name="posts"),
    path("listing/<int:page_number>", views.listing, name="listing"),
    path("edit/<int:pk>/<str:content>", views.edit_post, name="edit"),
    path("like/<int:pk>", views.like, name="like"),
]
