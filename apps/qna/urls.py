from django.urls import path

from .views import (
    index,
    quiz_list_view,
    quiz_view,
    register_view,
    save_quiz_results,
    update_interest,
)
from .api import HomePageView

urlpatterns = [
    path("", index, name="index"),
    path("quiz/", quiz_view, name="quiz"),
    path("register/", register_view, name="register"),
    path("save-quiz-results/", save_quiz_results, name="save_quiz_results"),
    path("quiz-list/", quiz_list_view, name="quiz_list"),
    path("update-interest/", update_interest, name="update_interest"),
    path("api/v1/home/", HomePageView.as_view(), name="api_home"),
]
