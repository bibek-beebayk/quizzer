from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.qna.models import Category, QuizResult


@login_required
def profile(request):
    context = {}
    # context['user'] = request.user
    context["total_quizzes"] = request.user.total_quizzes_taken
    context["average_score"] = request.user.average_score
    context["highest_score"] = request.user.highest_score
    context["highest_score_quiz"] = request.user.highest_score_quiz
    context["lowest_score"] = request.user.lowest_score
    context["lowest_score_quiz"] = request.user.lowest_score_quiz
    context["monthly_quizzes"] = request.user.quizzes_this_month
    context["most_active_category"] = request.user.most_active_category
    context["total_questions"] = request.user.total_questions_answered
    context["correct_answers"] = request.user.total_correct_answers
    context["recent_quizzes"] = QuizResult.objects.filter(user=request.user).order_by(
        "-created_at"
    )[:5]
    context["all_interests"] = Category.objects.all().order_by("name")
    # context["user_interests"] = request.user.interests.values_list("category", flat=True)
    return render(request, "profile.html", context)
