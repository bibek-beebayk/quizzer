from django.shortcuts import render
from apps.analytics.models import PageVisit
from core.libs.decorators import superadmin_required
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


@superadmin_required(login_url="/")
def analytics_dashboard(request):
    context = {}
    context["page_visit_data"] = PageVisit.get_page_visit_data()
    context["registration_data"] = User.get_registration_data()
    return render(request, "analytics/index.html", context)