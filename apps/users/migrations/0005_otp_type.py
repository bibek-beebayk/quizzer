# Generated by Django 5.0 on 2025-02-02 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_otp"),
    ]

    operations = [
        migrations.AddField(
            model_name="otp",
            name="type",
            field=models.CharField(default="password_reset", max_length=32),
        ),
    ]
