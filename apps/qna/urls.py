from django.urls import path

from .views import (
    index,
    login_view,
    logout_view,
    quiz_list_view,
    quiz_view,
    register_view,
    save_quiz_results,
    update_interest,
)

urlpatterns = [
    path("", index, name="index"),
    path("quiz/", quiz_view, name="quiz"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("save_quiz_results/", save_quiz_results, name="save_quiz_results"),
    path("quiz-list/", quiz_list_view, name="quiz_list"),
    path("update-interest/", update_interest, name="update_interest"),
]
