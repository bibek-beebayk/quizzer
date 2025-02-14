from django.contrib import admin

from .models import User, RequestLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    )
    list_display_links = ("id", "username")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name")
    list_per_page = 25
    ordering = ("id",)

    def save_model(self, request, obj, form, change) -> None:
        password = request.POST.get("password")
        if not (
            form.initial.get("password") and form.initial.get("password") == password
        ):
            obj.set_password(password)
        return super().save_model(request, obj, form, change)


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "endpoint",
        "user",
        "response_code",
        "method",
        "remote_address",
        "exec_time",
        "date",
    )
    list_display_links = ("id", "endpoint")
    list_filter = ("response_code", "method")
    search_fields = ("endpoint", "user", "remote_address")
    list_per_page = 25
    ordering = ("-id",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
