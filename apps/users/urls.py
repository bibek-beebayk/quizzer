from django.urls import path
from .views import profile, login_view, logout_view, change_password

urlpatterns = [
    path("profile/", profile, name="profile"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("change-password/", change_password, name="change_password"),
]
