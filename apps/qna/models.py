from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

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
    publish_at = models.DateTimeField(default=timezone.now)

    @property
    def has_quiz(self):
        return self.quizzes.exists()

    def __str__(self):
        return f"{self.question_text} - {self.categories.first()} - {self.has_quiz}"

    @classmethod
    def published(cls):
        return cls.objects.filter(publish_at__lte=timezone.now())

    @classmethod
    def random_question(cls, user):
        if not user.is_authenticated:
            return cls.published().order_by("?").first()
        user_interests = user.interests.all()
        if not user_interests.exists():
            return cls.published().order_by("?").first()
        return (
            cls.published().filter(categories__in=user_interests).order_by("?").first()
        )

    @property
    def categories_str(self):
        return ", ".join([category.name for category in self.categories.all()])


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
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="quizzes",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    publish_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.pk:
            old_quiz = Quiz.objects.get(pk=self.pk)
            if old_quiz.publish_at != self.publish_at:
                self.questions.update(publish_at=self.publish_at)
        if not self.category_id:
            self.category = Category.objects.get_or_create(name="Random")[0]
        return super().save(*args, **kwargs)

    @classmethod
    def published(cls):
        return cls.objects.filter(publish_at__lte=timezone.now())

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Quizzes"


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
    category = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        if self.quiz:
            self.quiz_name = self.quiz.name
        if not self.percentage:
            self.percentage = self.score
        if not self.category:
            if self.quiz:
                self.category = self.quiz.category.name
            else:
                self.category = self.quiz_name.split("Quiz")[0].strip()
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
