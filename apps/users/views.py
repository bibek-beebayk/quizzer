import json

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import redirect, render

from apps.analytics.models import PageVisit
from apps.qna.models import Category, QuizResult
from apps.users.models import Otp

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

    PageVisit.create_object(request)

    return render(request, "auth/login.html")


@login_required
def logout_view(request):
    request.session.flush()
    logout(request)
    return redirect("index")


def password_reset_email_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            user.generate_otp("password_reset")
            messages.success(request, "Password reset email sent.")
            return redirect("otp_input")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
    PageVisit.create_object(request)
    return render(request, "auth/password_reset.html")


def otp_input_view(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        try:
            otp_obj = Otp.objects.get(code=otp, is_used=False)
            otp_obj.is_used = True
            return redirect(f"/new-password-input/?email={otp_obj.user.email}")
        except Otp.DoesNotExist:
            messages.error(request, "Invalid OTP.")
    PageVisit.create_object(request)
    return render(request, "auth/otp_input.html")


def new_password_input_view(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password == confirm_password:
            # user = request.user
            # user.set_password(password)
            # user.save()
            # login(request, user)
            email = request.GET.get("email")
            user = User.objects.get(email=email)
            user.set_password(password)
            # login(request, user)
            user.save()
            messages.success(request, "Password reset successful.")
            return redirect("login")
        else:
            messages.error(request, "Passwords do not match.")
    PageVisit.create_object(request)
    return render(request, "auth/new_password_input.html")


@login_required
def profile(request):
    context = {}
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
    context["recent_quizzes"] = (
        QuizResult.objects.select_related("quiz")
        .filter(user=request.user)
        .order_by("-created_at")[:5]
    )
    context["all_interests"] = Category.objects.all().order_by("name")
    PageVisit.create_object(request)
    return render(request, "profile.html", context)


@login_required
def change_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = PasswordChangeForm(request.user, data)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return JsonResponse({"success": True})
        else:
            # Collect and return error messages
            errors = form.errors.get_json_data()
            return JsonResponse(
                {"success": False, "error": next(iter(errors.values()))[0]["message"]}
            )

    return JsonResponse({"success": False, "error": "Invalid request"})
