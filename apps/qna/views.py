import random

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from apps.qna.models import Category, Question


def index(request):
    context = {}
    random_question = Question.random_question()
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
    context = {}
    if category_id == "random":
        questions = Question.objects.order_by("?")[:10]
    else:
        category = Category.objects.get(id=category_id)
        questions = category.questions.order_by("?")[:10]
        context["category"] = category
    for question in questions:
        answers = list(question.answers.all())
        random.shuffle(answers)
        question.shuffled_answers = answers
    context["questions"] = questions
    context["questions_count"] = len(questions)
    context["total_weightage"] = questions.aggregate(total_weightage=Sum("weightage"))[
        "total_weightage"
    ]
    return render(request, "quiz.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # if username == "admin" and password == "admin":
        #     return render(request, 'admin.html')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Invalid credentials")
        except User.DoesNotExist:
            messages.error(request, "Username does not exist.")
    return render(request, "login.html")


@login_required
def logout_view(request):
    request.session.flush()
    logout(request)
    return redirect("index")
