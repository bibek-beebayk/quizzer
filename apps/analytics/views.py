from django.shortcuts import render
from core.libs.decorators import superadmin_required


@superadmin_required(login_url="/")
def analytics_dashboard(request):
    return render(request, "analytics/index.html")