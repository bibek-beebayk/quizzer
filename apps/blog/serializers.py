from rest_framework import serializers
from .models import Blog


class BlogListSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            "id",
            "title",
            "slug",
            "cover_image",
            "publish_at",
            "reading_time",
        )
        read_only_fields = fields

class BlogDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            "id",
            "title",
            "slug",
            "cover_image",
            "publish_at",
            "reading_time",
            "content",
        )
        read_only_fields = fields