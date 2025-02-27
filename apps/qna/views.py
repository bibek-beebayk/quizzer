import datetime
import json
import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError, transaction
from django.db.models import Count, Exists, FloatField, OuterRef, Subquery, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.analytics.models import PageVisit
from apps.blog.models import Blog
from apps.qna.models import Category, Question, Quiz, QuizResult

User = get_user_model()


def index(request):
    context = {}
    random_question = Question.random_question(request.user)

    if request.user.pk:
        categories = (
            request.user.interests.prefetch_related("questions")
            .annotate(qc=Count("questions"))
            .filter(qc__gte=10)
            .order_by("name")
        )
    else:
        categories = (
            Category.objects.prefetch_related("questions")
            .annotate(qc=Count("questions"))
            .filter(qc__gte=10)
            .order_by("name")
        )
    if random_question:
        answers = list(random_question.answers.all())
        random.shuffle(answers)
        random_question.shuffled_answers = answers
        context["random_question"] = random_question
        context["random_question_correct_answer"] = random_question.answers.get(
            is_correct=True
        )
    context["categories"] = categories
    if not request.user.pk:
        context["questions_count"] = Question.published().count()
    else:
        context["questions_count"] = request.user.interests.annotate(
            questions_count=Count("questions")
        ).aggregate(total_questions=Sum("questions_count"))["total_questions"]
    context["recent_blogs"] = Blog.published().order_by("-created_at")[:4]
    context["all_categories"] = Category.objects.order_by("name")

    # Create Page View Object
    PageVisit.create_object(request)
    return render(request, "index.html", context)


def quiz_view(request):
    context = {}
    questions = None
    quiz_id = None
    if request.method == "GET":
        category_id = request.GET.get("category")
        quiz_id = request.GET.get("quiz")
        if category_id:
            if category_id == "random":
                if request.user.pk:
                    questions = (
                        Question.published()
                        .filter(categories__in=request.user.interests.all())
                        .order_by("?")[:10]
                    )
                else:
                    questions = Question.published().order_by("?")[:10]
                quiz_name = "Random Quiz"
            else:
                category = Category.objects.get(id=category_id)
                questions = (
                    Question.published().filter(categories=category).order_by("?")[:10]
                )
                context["category"] = category
                quiz_name = category.name + " Quiz"
        elif quiz_id:
            if not request.user.is_authenticated:
                messages.error(request, "Please login or signup to take quiz.")
                return redirect("login")
            user_quiz_results = QuizResult.objects.filter(
                user=request.user
            ).values_list("quiz_id", flat=True)
            if int(quiz_id) in user_quiz_results:
                messages.error(
                    request,
                    "You have already taken this quiz. Here are some quizes that you can take now.",
                )
                base_url = reverse("quiz_list")
                params = "taken=not-taken"
                return redirect(f"{base_url}?{params}")
            try:
                quiz = Quiz.objects.get(id=quiz_id)
            except Quiz.DoesNotExist:
                messages.error(request, "Quiz not found.")
                return redirect("/quiz-list/?taken=not-taken")
            questions = quiz.questions.prefetch_related("answers").order_by("?")
            quiz_name = quiz.name
            context["quiz_id"] = quiz_id

    elif request.method == "POST":
        categories = request.POST.getlist("interests")
        count = int(request.POST.get("count"))
        questions = (
            Question.objects.prefetch_related("answers")
            .filter(categories__in=categories)
            .order_by("?")[:count]
        )
        quiz_name = "Custom Quiz"

    if not questions or questions.count() == 0:
        messages.error(request, "No questions found. Try these quizzes instead.")
        return redirect("/quiz-list/?taken=not-taken")

    for question in questions:
        answers = list(question.answers.all())
        random.shuffle(answers)
        question.shuffled_answers = answers
    context["questions"] = questions
    context["questions_count"] = len(questions)
    context["total_weightage"] = questions.aggregate(total_weightage=Sum("weightage"))[
        "total_weightage"
    ]
    context["quiz_name"] = quiz_name

    PageVisit.create_object(request, quiz_id)

    return render(request, "quiz.html", context)


def verify_registration(request):
    signed_data = request.GET.get("data")

    if not signed_data:
        return HttpResponse("Invalid request. Please try again.")

    try:
        data = signing.loads(signed_data)
        email = data.get("email")
        password = data.get("password")
        interests = data.get("interests")
        exp_timestamp = data.get("exp")
        exp_time = datetime.datetime.fromtimestamp(
            exp_timestamp, tz=datetime.timezone.utc
        )

        if timezone.now() > exp_time:
            return HttpResponse("Link expired. Please try again.")
    except signing.BadSignature:
        return HttpResponse("Invalid link. Please try again.")

    try:
        with transaction.atomic():
            user = User.objects.create_user(email=email, password=password)
            user.interests.set([int(interest) for interest in interests])
            send_mail(
                "New User Registration",
                f"New user registered with email {user.email}",
                settings.EMAIL_HOST_USER,
                ["quiznfacts2024@gmail.com"],
                fail_silently=False,
            )
            login(request, user)
            return redirect("index")
    except IntegrityError as e:
        messages.error(request, "Email already exists.")
        return redirect("register")


def register_view(request):
    context = {}
    context["interests"] = Category.objects.order_by("name")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        interests = request.POST.getlist("interests")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:

            exp_time = timezone.now() + timezone.timedelta(minutes=10)
            exp_timestamp = exp_time.timestamp()

            data = {
                "email": email,
                "password": password,
                "interests": interests,
                "exp": exp_timestamp,
            }
            signed_data = signing.dumps(data)
            regn_link = (
                request.build_absolute_uri(reverse("verify_registration"))
                + f"?data={signed_data}"
            )
            send_mail(
                "Verify Registration",
                f"Follow this link to verify your registration. The link will expire in 10 minutes. {regn_link}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return HttpResponse(
                "Verification link sent to your email. Click on the link to verify your registration. The link will expire in 10 minutes. You can close this page now."
            )
    PageVisit.create_object(request)
    return render(request, "auth/register.html", context)


@require_POST
@login_required
def save_quiz_results(request):
    try:
        data = json.loads(request.body)
        quiz_id = data.pop("quiz_id")
        data["quiz_id"] = int(quiz_id) if quiz_id else None
        quiz_result = QuizResult.objects.create(user=request.user, **data)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@login_required
def quiz_list_view(request):
    category_id = request.GET.get("category")
    taken = request.GET.get("taken")
    # Base queryset for quizzes
    quizzes = Quiz.published().annotate(
        is_taken=Exists(
            QuizResult.objects.filter(user=request.user, quiz=OuterRef("pk"))
        ),
        user_score_percentage=Subquery(
            QuizResult.objects.filter(user=request.user, quiz=OuterRef("pk")).values(
                "percentage"
            )[:1],
            output_field=FloatField(),
        ),
    )

    if category_id:
        quizzes = quizzes.filter(category_id=category_id)

    if taken == "taken":
        quizzes = quizzes.filter(is_taken=True)
    elif taken == "not-taken":
        quizzes = quizzes.filter(is_taken=False)

    quizzes = quizzes.order_by("-created_at")
    # Pagination
    paginator = Paginator(quizzes, 10)
    page = request.GET.get("page", 1)

    try:
        paginated_quizzes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_quizzes = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        paginated_quizzes = paginator.page(paginator.num_pages)

    context = {
        "quizzes": paginated_quizzes,
        "categories": Category.objects.filter(quizzes__isnull=False)
        .distinct()
        .order_by("name"),
        "total_quiz_count": Quiz.objects.count(),
        "category_id": category_id,  # Pass category_id to maintain filter in pagination
    }

    PageVisit.create_object(request)
    return render(request, "quiz_list.html", context)


@require_POST
@login_required
def update_interest(request):
    try:
        data = json.loads(request.body)
        interest_ids = data.get("interests", [])
        interest_ids = [int(id) for id in interest_ids]
        user = request.user
        user.interests.clear()
        user.interests.add(*Category.objects.filter(id__in=interest_ids))
        return JsonResponse({"status": "success"})
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
