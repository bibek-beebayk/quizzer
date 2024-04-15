import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.db import IntegrityError

from apps.qna.models import Category

question_categories = [
    "History",
    "Geography",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer Science",
    "Arts",
    "Music",
    "Sports",
    "Technology",
    "Movies",
    "TV",
    "Games",
    "Other",
]

for category in question_categories:
    try:
        Category.objects.create(name=category)
    except IntegrityError:
        print(f"Category {category} already exists")
        continue
    print(f"Created category {category}")
