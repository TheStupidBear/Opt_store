from django.urls import path, include
from . import views

from .views import (
    User_login,
    Register,
    Profile,
)

app_name = "users"
urlpatterns = [
    # страница входа пользователя
    path("login/", User_login.as_view(), name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", Register.as_view(), name="register"),
    path("profile/", Profile.as_view(), name="profile"),
]
