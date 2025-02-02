from django.urls import path
from .views import add_blog_comment


urlpatterns = [
    path("add-blog-comment/<int:blog_id>/", add_blog_comment, name="add_blog_comment"),
]
