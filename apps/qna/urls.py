from django.urls import path
from .views import index, quiz_view, login_view, logout_view


urlpatterns = [
    path('', index, name='index'),
    path('quiz/', quiz_view, name='quiz'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]