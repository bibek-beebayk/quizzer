from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import BlogListSerialzier, BlogDetailSerializer
from .models import Blog


class BlogViewSet(ReadOnlyModelViewSet):
    serializer_class = BlogListSerialzier
    queryset = Blog.published().order_by("-created_at")
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BlogDetailSerializer
        return super().get_serializer_class()
