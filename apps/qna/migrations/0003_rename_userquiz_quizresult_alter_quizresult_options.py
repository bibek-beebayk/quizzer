# Generated by Django 5.1.5 on 2025-01-24 08:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("qna", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UserQuiz",
            new_name="QuizResult",
        ),
        migrations.AlterModelOptions(
            name="quizresult",
            options={},
        ),
    ]
