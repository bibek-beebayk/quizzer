from apps.interaction.models import Comment
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
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
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=256)
    content = CKEditor5Field(config_name="default")
    categories = models.ManyToManyField(BlogCategory, related_name="blogs")
    cover_image = models.ImageField(upload_to="blog_covers/", blank=True, null=True)
    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="blogs",
        blank=True,
        null=True,
    )
    excerpt = models.TextField(blank=True, null=True)
    keywords = models.CharField(
        max_length=256,
        default="interesting blog, general knowledge, facts, interesting facts, random facts",
        blank=True,
    )

    publish_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = GenericRelation(Comment)

    @property
    def category_str(self):
        # return ", ".join([f"<a style='cursor:pointer;' href='/'>{category.name}</a>" for category in self.categories.all()])
        return ", ".join([category.name for category in self.categories.all()])

    @property
    def reading_time(self):
        return calculate_reading_time(self.content)

    def get_absolute_url(self):
        url = reverse("blog", kwargs={"slug": self.slug})
        return url

    def __str__(self):
        return self.title
