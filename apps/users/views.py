import json
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.qna.models import Category, QuizResult

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Invalid credentials")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
    return render(request, "login.html")


@login_required
def logout_view(request):
    request.session.flush()
    logout(request)
    return redirect("index")


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

from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = PasswordChangeForm(request.user, data)
        
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return JsonResponse({'success': True})
        else:
            # Collect and return error messages
            errors = form.errors.get_json_data()
            return JsonResponse({
                'success': False, 
                'error': next(iter(errors.values()))[0]['message']
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})