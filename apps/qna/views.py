from django.shortcuts import render

from apps.qna.models import Category, Question
from django.db.models import Count
from django.db.models import Sum
import random


def index(request):
    context = {}
    random_question = Question.random_question()
    categories = Category.objects.annotate(questions_count=Count('questions')).filter(questions_count__gt=0).order_by("name")
    if random_question:
        context["random_question"] = random_question
        context["random_question_correct_answer"] = random_question.answers.get(is_correct=True)
    context["categories"] = categories 
    return render(request, 'index.html', context)


def quiz_view(request, category_id):
    context = {}
    category = Category.objects.get(id=category_id)
    questions = category.questions.order_by("?")[:10]
    for question in questions:
        answers = list(question.answers.all())
        random.shuffle(answers)
        question.shuffled_answers = answers
    context["category"] = category
    context["questions"] = questions
    context["questions_count"] = len(questions)
    context["total_weightage"] = questions.aggregate(total_weightage=Sum('weightage'))["total_weightage"]
    return render(request, 'quiz.html', context)
