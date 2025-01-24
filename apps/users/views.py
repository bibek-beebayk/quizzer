from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.qna.models import QuizResult


@login_required
def profile(request):
    context = {}
    # context['user'] = request.user
    context["total_quizzes"] = 24
    context["average_score"] = 70
    context["highest_score"] = 90
    context["highest_score_quiz"] = "Django Quiz"
    context["lowest_score"] = 30
    context["lowest_score_quiz"] = "Python Quiz"
    context["monthly_quizzes"] = 12
    context["most_active_category"] = "Python"
    context["total_questions"] = 120
    context["correct_answers"] = 85
    context["recent_quizzes"] = QuizResult.objects.filter(user=request.user).order_by(
        "-created_at"
    )[:5]
    return render(request, "profile.html", context)
