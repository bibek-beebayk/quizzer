from rest_framework import serializers
from .models import Answer, Category, Question


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "answer_text", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    
    def get_answers(self, obj):
        answers = obj.answers.order_by("?")
        return AnswerSerializer(answers, many=True).data
    
    class Meta:
        model = Question
        fields = ["id", "question_text", "answers", "categories_str"]


# class HomePageSerializer(serializers.Serializer):
#     random_question = serializers.SerializerMethodField()

#     def get_random_question(self, obj):
#         import ipdb; ipdb.set_trace()
#         return Question.objects.random_question(self.context["request"].user)
