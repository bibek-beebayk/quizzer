# Generated by Django 5.0.3 on 2024-04-26 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qna", "0009_alter_collection_questions_alter_quiz_questions"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="answer_explanation",
            field=models.TextField(blank=True, null=True),
        ),
    ]
