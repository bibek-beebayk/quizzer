from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Blog, BlogCategory


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = ("content",)
