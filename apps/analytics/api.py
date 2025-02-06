from .models import WebsiteAnalytics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action


class AnalyticsViewSet(GenericViewSet):
    # def get_queryset(self):
    #     return None
    
    # def get_serializer_class(self):
    #     return None

    @action(methods=["GET"], detail=False)
    def dashboard(self, request, *args, **kwargs):
        analytics = WebsiteAnalytics()
        response = {
            "total_visits_today": analytics.total_visits_today(),
            "daily_traffic": analytics.daily_traffic(7),
            "popular_pages": analytics.popular_pages(5),
            "user_engagement": analytics.user_engagement(),
            "hourly_distribution": analytics.hourly_distribution(),
            "bounce_rate": analytics.bounce_rate(),
            "retention_analysis": analytics.retention_analysis(),
        }
        return Response(response)
