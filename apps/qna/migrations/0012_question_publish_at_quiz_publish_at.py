# Generated by Django 5.1.5 on 2025-01-26 09:33

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qna", "0011_delete_userinterest"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="publish_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="quiz",
            name="publish_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
