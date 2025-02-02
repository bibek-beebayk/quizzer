from django.urls import path
from .views import profile, login_view, logout_view, change_password, password_reset_email_view, otp_input_view, new_password_input_view

urlpatterns = [
    path("profile/", profile, name="profile"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("change-password/", change_password, name="change_password"),
    path("password-reset-email/", password_reset_email_view, name="password_reset_email"),
    path("otp-input/", otp_input_view, name="otp_input"),
    path("new-password-input/", new_password_input_view, name="new_password_input"),
]
