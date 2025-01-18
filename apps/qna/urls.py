from django.urls import path
from .views import index, quiz_view


urlpatterns = [
    path('', index, name='index'),
    path('quiz/', quiz_view, name='quiz'),
]