# Generated by Django 5.0 on 2025-02-04 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analytics", "0007_pagevisit_query_params"),
    ]

    operations = [
        migrations.AddField(
            model_name="pagevisit",
            name="client_ip",
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
