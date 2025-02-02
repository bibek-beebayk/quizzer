from apps.qna.models import Category, Question
from .serializers import CategorySerializer, QuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class HomePageView(APIView):

    def get(self, request):
        res = {}
        res["random_question"] = QuestionSerializer(Question.random_question(request.user)).data
        res["categories"] = CategorySerializer(Category.get_by_user(request.user), many=True).data
        return Response(res)
