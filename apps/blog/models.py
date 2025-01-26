from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


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
    category = models.ForeignKey(
        BlogCategory, on_delete=models.CASCADE, related_name="blogs"
    )
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

    def __str__(self):
        return self.title
