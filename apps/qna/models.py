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

    def __str__(self):
        return self.question_text
    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


class Collection(models.Model):
    name = models.CharField(max_length=100, unique=True)
    questions = models.ManyToManyField(Question, related_name="collections")

    def __str__(self) -> str:
        return self.name