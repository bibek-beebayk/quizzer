from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import Blog
from apps.qna.models import Quiz
from django.utils import timezone


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return ["index", "blogs", "quiz_list"]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Blog.objects.filter(publish_at__lte=timezone.now()).order_by(
            "-publish_at"
        )

    def lastmod(self, obj):
        return obj.updated_at


class QuizSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Quiz.objects.filter(publish_at__lte=timezone.now()).order_by(
            "-publish_at"
        )

    def lastmod(self, obj):
        return obj.created_at


class Sitemaps(dict):
    def __init__(self, *args, **kwargs):
        super(Sitemaps, self).__init__(*args, **kwargs)
        self["static"] = StaticViewSitemap
        self["blogs"] = BlogSitemap
        self["quizzes"] = QuizSitemap
