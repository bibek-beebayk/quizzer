from django.urls import path
from .views import index, quiz_view, login_view, logout_view, register_view, save_quiz_results


urlpatterns = [
    path('', index, name='index'),
    path('quiz/', quiz_view, name='quiz'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('save_quiz_results/', save_quiz_results, name='save_quiz_results'),
]