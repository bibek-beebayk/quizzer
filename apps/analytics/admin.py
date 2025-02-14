from django.contrib import admin

from .models import PageVisit


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = (
        "page",
        "url",
        "client_ip",
        "query_params",
        "user",
        "obj_id",
        "created_at",
    )
    list_filter = ("page", "created_at")
    search_fields = ("user__username", "page")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
