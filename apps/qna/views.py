import json
import random

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.qna.models import Category, Question, Quiz, QuizResult, UserInterest

User = get_user_model()


def index(request):
    context = {}
    random_question = Question.random_question(request.user)
    categories = (
        Category.objects.annotate(questions_count=Count("questions"))
        .filter(questions_count__gt=0)
        .order_by("name")
    )
    if random_question:
        context["random_question"] = random_question
        context["random_question_correct_answer"] = random_question.answers.get(
            is_correct=True
        )
    context["categories"] = categories
    context["questions_count"] = Question.objects.count()
    return render(request, "index.html", context)


def quiz_view(request):
    category_id = request.GET.get("category")
    quiz_id = request.GET.get("quiz")
    context = {}
    if category_id:
        if category_id == "random":
            questions = Question.objects.order_by("?")[:10]
            quiz_name = "Random Quiz"
        else:
            category = Category.objects.get(id=category_id)
            questions = category.questions.order_by("?")[:10]
            context["category"] = category
            quiz_name = category.name + " Quiz"
    elif quiz_id:
        quiz = Quiz.objects.get(id=quiz_id)
        questions = quiz.questions.order_by("?")
        quiz_name = quiz.name
        context["quiz_id"] = quiz_id

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
    return render(request, "quiz.html", context)


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


from django.db import IntegrityError, transaction


@transaction.atomic
def register_view(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        interests = request.POST.getlist("interests")

        try:
            with transaction.atomic():
                user = User.objects.create_user(email=email, password=password)
                for interest_id in interests:
                    category = Category.objects.get(id=interest_id)
                    UserInterest.objects.create(user=user, category=category)
                login(request, user)
                return redirect("index")
        except IntegrityError as e:
            messages.error(request, "Email already exists.")

    context["interests"] = Category.objects.order_by("name")
    return render(request, "register.html", context)


@require_POST
@login_required
def save_quiz_results(request):
    try:
        data = json.loads(request.body)
        # import ipdb; ipdb.set_trace()
        quiz_id = data.pop("quiz_id")
        data["quiz_id"] = int(quiz_id) if quiz_id else None
        quiz_result = QuizResult.objects.create(user=request.user, **data)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def quiz_list_view(request):
    category_id = request.GET.get("category")
    
    # Base queryset for quizzes
    quizzes = (
        Quiz.objects.filter(category_id=category_id)
        if category_id
        else Quiz.objects.all()
    ).order_by("-created_at")
    
    # Pagination
    paginator = Paginator(quizzes, 5)  # Show 10 quizzes per page
    page = request.GET.get('page', 1)
    
    try:
        paginated_quizzes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_quizzes = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        paginated_quizzes = paginator.page(paginator.num_pages)
    
    context = {
        'quizzes': paginated_quizzes,
        'categories': Category.objects.filter(quizzes__isnull=False).distinct().order_by("name"),
        'total_quiz_count': Quiz.objects.count(),
        'category_id': category_id  # Pass category_id to maintain filter in pagination
    }
    
    return render(request, "quiz_list.html", context)
