from django.urls import path
from .views import blog_list_view, blog_detail_view, edit_comment, delete_comment

urlpatterns = [
    path("blogs/", blog_list_view, name="blogs"),
    path("blogs/<slug:slug>/", blog_detail_view, name="blog"),
    path("edit-comment/", edit_comment, name="edit_comment"),
    path("delete-comment/", delete_comment, name="delete_comment"),
]