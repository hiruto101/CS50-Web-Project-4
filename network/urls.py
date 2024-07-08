
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile",views.profile, name="profile"),
    path("post", views.post, name="post"),
    path("like/<int:post_id>", views.like, name="like"),
    path("edit/<int:post_id>", views.edit, name="edit"),
]
