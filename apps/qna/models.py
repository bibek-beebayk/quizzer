from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.TextField()
    question_image = models.ImageField(
        upload_to="questions/images/", blank=True, null=True
    )
    question_audio = models.FileField(
        upload_to="questions/audios/", blank=True, null=True
    )
    categories = models.ManyToManyField(Category, related_name="questions")
    tags = models.ManyToManyField(Tag, related_name="questions", blank=True)
    hint = models.TextField(blank=True, null=True)
    answer_explanation = models.TextField(blank=True, null=True)
    weightage = models.FloatField(default=1.0)
    difficulty = models.CharField(
        max_length=50,
        choices=(("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")),
        default="Easy",
    )

    def __str__(self):
        return self.question_text

    @classmethod
    def random_question(cls):
        return cls.objects.order_by("?").first()


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    answer_image = models.ImageField(blank=True, null=True, upload_to="answers/images/")

    def __str__(self):
        return self.answer_text


class Collection(models.Model):
    name = models.CharField(max_length=100, unique=True)
    questions = models.ManyToManyField(Question, related_name="collections", blank=True)

    def __str__(self) -> str:
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=100, unique=True)
    questions = models.ManyToManyField(Question, related_name="quizzes", blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Quizzes"


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interests")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="interests"
    )

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="users", blank=True, null=True
    )
    quiz_name = models.CharField(max_length=100, blank=True, null=True)
    time_spent = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    attempted_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    answers = models.JSONField(default=list)
    percentage = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if self.quiz:
            self.quiz_name = self.quiz.name
        if not self.percentage:
            self.percentage = self.score
        super().save(*args, **kwargs)

    @property
    def score(self):
        if self.quiz:
            sc = (self.correct_answers / self.quiz.questions.count()) * 100
        elif self.total_questions == 0:
            sc = 0
        else: 
            sc = (self.correct_answers / self.total_questions) * 100
        return round(sc, 2)

    def __str__(self):
        if self.quiz:
            return f"{self.user.username} - {self.quiz.name}"
        else:
            return f"{self.user.username} - {self.quiz_name}"
