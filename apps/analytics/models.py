from django.db import models

from core.libs.utils import get_client_ip
from django.utils import timezone
from django.db.models.functions import TruncDate, TruncHour, ExtractHour


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
    elif url.startswith("/quiz-list/"):
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
        on_delete=models.SET_NULL,
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
            client_ip=get_client_ip(request),
        )

    @classmethod
    def get_page_visit_data(cls):
        # pages_vivits_coo = cls.objects.all().values('page').annotate(count=models.Count('page'))
        response_data = {}
        response_data["total_page_visits"] = cls.objects.count()
        response_data["total_page_visits_today"] = cls.objects.filter(
            created_at__date=timezone.now().date()
        ).count()
        response_data["page_visits_last_7_days"] = cls.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).count()
        response_data["page_visits_last_30_days"] = cls.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=30)
        ).count()
        return response_data

    def __str__(self):
        return self.page

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class WebsiteAnalytics:
    def __init__(self, queryset=None):
        self.queryset = queryset if queryset else PageVisit.objects.all()

    def daily_traffic(self, days=30):
        return (
            self.queryset.annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(visits=models.Count("id"))
            .order_by("-date")[:days]
        )

    def popular_pages(self, limit=10):
        return (
            self.queryset.values("page")
            .annotate(
                total_visits=models.Count("id"),
                unique_visitors=models.Count("user", distinct=True),
                unique_ips=models.Count("client_ip", distinct=True),
            )
            .order_by("-total_visits")[:limit]
        )

    def user_engagement(self):
        return (
            self.queryset.exclude(user=None)
            .values("user")
            .annotate(
                visit_count=models.Count("id"),
                first_visit=models.Min("created_at"),
                last_visit=models.Max("created_at"),
                unique_pages=models.Count("page", distinct=True),
            )
            .order_by("-visit_count")
        )

    def hourly_distribution(self):
        qs = (
            self.queryset.annotate(hour=ExtractHour("created_at"))
            .values("hour")
            .annotate(visits=models.Count("id"))
            .order_by("hour")
        )

        data_init = [{"hour": x, "visits": 0} for x in range(0, 24)]

        for obj in qs:
            data_init[obj["hour"]]["hour"] = obj["hour"]
            data_init[obj["hour"]]["visits"] = obj["visits"]
        return data_init

    def bounce_rate(self):
        """Calculate bounce rate (users with single page visit)."""
        total_sessions = self.queryset.values("client_ip", "user").distinct().count()

        bounce_sessions = (
            self.queryset.values("client_ip", "user")
            .annotate(pages=models.Count("page"))
            .filter(pages=1)
            .count()
        )

        return {
            "total_sessions": total_sessions,
            "bounce_sessions": bounce_sessions,
            "bounce_rate": (
                round((bounce_sessions / total_sessions * 100), 2)
                if total_sessions > 0
                else 0
            ),
        }

    def retention_analysis(self, days=30):
        """Analyze user retention over time."""
        today = timezone.now().date()
        start_date = today - timezone.timedelta(days=days)

        return (
            self.queryset.filter(created_at__date__gte=start_date)
            .exclude(user=None)
            .values("user")
            .annotate(
                first_visit_date=TruncDate(models.Min("created_at")),
                days_active=models.Count("created_at__date", distinct=True),
                last_visit_date=TruncDate(models.Max("created_at")),
            )
            .order_by("first_visit_date")
        )

    def total_visits_today(self):
        return self.queryset.filter(created_at__date=timezone.now().date()).count()
