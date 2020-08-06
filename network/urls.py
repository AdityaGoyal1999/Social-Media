
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-post", views.create_post, name="create_post"),
    path("all-posts", views.all_posts_view, name="all_posts"),
    path("posts", views.posts, name="posts"),
]
