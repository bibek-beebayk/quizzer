from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

from core.libs.utils import calculate_reading_time


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Categories"


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = CKEditor5Field(config_name="extends")
    categories = models.ManyToManyField(BlogCategory, related_name="blogs")
    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="blogs",
        blank=True,
        null=True,
    )
    publish_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def category_str(self):
        return ", ".join([f"<a style='cursor:pointer;' href='/'>{category.name}</a>" for category in self.categories.all()])

    @property
    def reading_time(self):
        return calculate_reading_time(self.content)

    def __str__(self):
        return self.title
