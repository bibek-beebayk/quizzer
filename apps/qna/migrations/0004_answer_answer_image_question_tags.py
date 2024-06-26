# Generated by Django 5.0.3 on 2024-04-17 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qna", "0003_tag_alter_category_options_remove_question_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="answer_image",
            field=models.ImageField(blank=True, null=True, upload_to="answers/images/"),
        ),
        migrations.AddField(
            model_name="question",
            name="tags",
            field=models.ManyToManyField(related_name="questions", to="qna.tag"),
        ),
    ]
