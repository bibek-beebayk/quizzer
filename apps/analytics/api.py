from .models import WebsiteAnalytics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render


class AnalyticsDashboardView(APIView):
    def get(self, request):
        analytics = WebsiteAnalytics()
        response = {
            "daily_traffic": analytics.daily_traffic(7),
            "popular_pages": analytics.popular_pages(),
            "user_engagement": analytics.user_engagement(),
            "hourly_distribution": analytics.hourly_distribution(),
            "bounce_rate": analytics.bounce_rate(),
            "retention_analysis": analytics.retention_analysis(),
        }
        return Response(response)
