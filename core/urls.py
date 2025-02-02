from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.sitemaps.views import sitemap
from .sitemaps import Sitemaps
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter

from apps.blog import api as blog_api

router = DefaultRouter()

router.register("blog", blog_api.BlogViewSet, basename="blog")

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /ckeditor5/",
        # "Sitemap: {}/sitemap.xml".format(settings.BASE_URL)
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("apps.qna.urls")),
        path("", include("pwa.urls")),
        path("", include("apps.users.urls")),
        path("", include("apps.blog.urls")),
        # path("__reload__/", include("django_browser_reload.urls")),
        path("ckeditor5/", include("django_ckeditor_5.urls")),
        # path("upload/", custom_upload_function, name="custom_upload_file"),
        path("summernote/", include("django_summernote.urls")),
        path("sitemap.xml", sitemap, {"sitemaps": Sitemaps()}, name="sitemap"),
        path('robots.txt', robots_txt),

        path("api/v1/", include(router.urls)),
        path("", include("apps.interaction.urls"))
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
