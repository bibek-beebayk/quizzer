from django.shortcuts import render

from apps.qna.models import Question


def index(request):
    context = {}
    random_question = Question.random_question()
    context["random_question"] = random_question
    context["random_question_correct_answer"] = random_question.answers.get(is_correct=True) 
    return render(request, 'index.html', context)
