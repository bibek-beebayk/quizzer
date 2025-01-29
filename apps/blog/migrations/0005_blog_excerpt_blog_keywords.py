# Generated by Django 5.0 on 2025-01-29 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_blog_cover_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="excerpt",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="blog",
            name="keywords",
            field=models.CharField(
                blank=True,
                default="interesting blog, general knowledge, facts, interesting facts, random facts",
                max_length=256,
            ),
        ),
    ]
