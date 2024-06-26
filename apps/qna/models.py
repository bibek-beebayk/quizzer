from django.db import models


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
    question_image = models.ImageField(upload_to='questions/images/', blank=True, null=True)
    question_audio = models.FileField(upload_to='questions/audios/', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name="questions")
    tags = models.ManyToManyField(Tag, related_name="questions", blank=True)
    hint = models.TextField(blank=True, null=True)
    answer_explanation = models.TextField(blank=True, null=True)
    weightage = models.FloatField(default=1.0)
    difficulty = models.CharField(max_length=50, choices=(("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")), default="Easy")

    def __str__(self):
        return self.question_text
    
    @classmethod
    def random_question(cls):
        return cls.objects.order_by('?').first()
    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
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