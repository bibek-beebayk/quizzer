from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("apps.qna.urls")),
        path("", include("pwa.urls")),
        path("", include("apps.users.urls")),
        path("", include("apps.blog.urls")),
        # path("__reload__/", include("django_browser_reload.urls")),
        path("ckeditor5/", include('django_ckeditor_5.urls')),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

