# Generated by Django 5.0.3 on 2024-04-22 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qna", "0008_alter_quiz_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="questions",
            field=models.ManyToManyField(
                blank=True, related_name="collections", to="qna.question"
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="questions",
            field=models.ManyToManyField(
                blank=True, related_name="quizzes", to="qna.question"
            ),
        ),
    ]