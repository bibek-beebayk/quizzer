# Generated by Django 5.0 on 2025-01-29 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qna", "0012_question_publish_at_quiz_publish_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="keywords",
            field=models.CharField(
                blank=True,
                default="quiz, general knowledge, test, mind test",
                max_length=256,
            ),
        ),
    ]
