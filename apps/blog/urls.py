from django.urls import path
from .views import blog_list_view

urlpatterns = [
    path("blogs/", blog_list_view, name="blogs"),
]
