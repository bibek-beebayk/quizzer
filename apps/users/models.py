from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True, null=True)

    def __str__(self):
        return self.user.email
    
