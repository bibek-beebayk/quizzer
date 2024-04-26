from django.shortcuts import render

from apps.qna.models import Category, Question
from django.db.models import Count


def index(request):
    context = {}
    random_question = Question.random_question()
    categories = Category.objects.annotate(questions_count=Count('questions')).filter(questions_count__gt=0).order_by("name")
    context["random_question"] = random_question
    context["random_question_correct_answer"] = random_question.answers.get(is_correct=True)
    context["categories"] = categories 
    return render(request, 'index.html', context)
