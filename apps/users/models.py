from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def total_quizzes_taken(self):
        return self.quizzes.count()

    @property
    def average_score(self):
        if self.total_quizzes_taken == 0:
            return 0
        total_score = sum(quiz.percentage for quiz in self.quizzes.all())
        return round(total_score / self.total_quizzes_taken, 2)

    @property
    def highest_score(self):
        if self.total_quizzes_taken == 0:
            return 0
        return max(quiz.percentage for quiz in self.quizzes.all())

    @property
    def highest_score_quiz(self):
        if self.highest_score == 0:
            return None
        return self.quizzes.filter(percentage=self.highest_score).first().quiz_name

    @property
    def lowest_score(self):
        if self.total_quizzes_taken == 0:
            return 0
        return min(quiz.percentage for quiz in self.quizzes.all())

    @property
    def lowest_score_quiz(self):
        if self.lowest_score == 0:
            return None
        return self.quizzes.filter(percentage=self.lowest_score).first().quiz_name

    @property
    def total_questions_answered(self):
        return sum(quiz.total_questions for quiz in self.quizzes.all())

    @property
    def total_correct_answers(self):
        return sum(quiz.correct_answers for quiz in self.quizzes.all())

    @property
    def most_active_category(self):
        categories = {}
        for quiz in self.quizzes.all():
            if quiz.category in categories:
                categories[quiz.category] += 1
            else:
                categories[quiz.category] = 1
        if not categories:
            return None
        return max(categories, key=categories.get)

    @property
    def quizzes_this_month(self):
        return self.quizzes.filter(created_at__month=timezone.now().month).count()


class RequestLog(models.Model):
    endpoint = models.CharField(
        max_length=1000, null=True
    )
    user = models.CharField(max_length=255)
    response_code = models.PositiveSmallIntegerField()
    method = models.CharField(max_length=10, null=True)
    remote_address = models.CharField(max_length=1000, null=True)
    exec_time = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now=True)
    body_response = models.TextField(null=True)
    body_request = models.TextField(null=True) 
    created_at = models.DateTimeField(auto_now_add=True)