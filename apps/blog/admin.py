from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Blog, BlogCategory, BlogSection


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


class BlogSectionInline(admin.StackedInline):
    model = BlogSection
    extra = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = ("content",)
    inlines = [BlogSectionInline]

