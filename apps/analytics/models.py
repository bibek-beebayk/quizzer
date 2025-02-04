from django.db import models

from core.libs.utils import get_client_ip


# class ActivityLog(models.Model):
#     user = models.ForeignKey(
#         "users.User",
#         on_delete=models.CASCADE,
#         related_name="activity_logs",
#         blank=True,
#         null=True,
#     )
#     # activity = models.CharField(max_length=255)
#     event = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)


def get_page_name(url):
    if url == "/":
        return "Home"
    elif url.startswith("/quiz/"):
        return "Quiz"
    elif url.startswith("/blogs/"):
        return "Blog"
    elif url.startswith("/quiz-llist/"):
        return "Quiz List"
    elif url.startswith("/profile/"):
        return "Profile"
    elif url.startswith("/login/"):
        return "Login"
    elif url.startswith("/register/"):
        return "Register"
    elif url.startswith("/password-reset-email/"):
        return "Password Reset Email"
    elif url.startswith("/otp-input/"):
        return "OTP Input"
    elif url.startswith("/new-password-input/"):
        return "New Password Input"
    return "Not Defined"

class PageVisit(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="page_visits",
        blank=True,
        null=True,
    )
    url = models.CharField(max_length=1000)
    query_params = models.JSONField(blank=True, null=True)
    page = models.CharField(max_length=255)
    obj_id = models.PositiveIntegerField(blank=True, null=True)
    client_ip = models.GenericIPAddressField(blank=True, null=True)
    extra_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_object(cls, request, obj_id=None):
        page = get_page_name(request.path)
        return cls.objects.create(
            page=page,
            url=request.path,
            user=request.user if request.user.pk else None,
            query_params=request.GET,
            obj_id=obj_id,
            client_ip = get_client_ip(request)
        )

    def __str__(self):
        return self.page

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
