from django.shortcuts import render
from apps.analytics.models import PageVisit
from core.libs.decorators import superadmin_required
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncHour
import pandas as pd
import plotly.express as px

User = get_user_model()


def get_hourly_visits_graph():
    now = timezone.now()
    twelve_hours_ago = now - timezone.timedelta(hours=12)

    hourly_visits = (
        PageVisit.objects.filter(
            created_at__gte=twelve_hours_ago
        )  # Filter visits in the last 12 hours
        .annotate(hour=TruncHour("created_at"))  # Truncate the timestamp to the hour
        .values("hour")  # Group by hour
        .annotate(visit_count=Count("id"))  # Count visits per hour
        .order_by("hour")  # Order by hour
    )

    hourly_data = {hour: 0 for hour in range(24)}

    for entry in hourly_visits:
        hour = entry["hour"].hour  # Extract the hour from the datetime object
        hourly_data[hour] = entry["visit_count"]

    hours = list(hourly_data.keys())[-12:]  # Last 12 hours
    visits = list(hourly_data.values())[-12:]

    df = pd.DataFrame({"Hour": hours, "Visits": visits})

    fig = px.line(
        df,
        x="Hour",
        y="Visits",
        title="Total Visits for last 12 hours",
        markers=True,
        labels={"Hour": "Hour of the day", "Visits": "Number of page visits"},
    )
    fig.update_layout(xaxis=dict(tickmode="linear", tick0=0, dtick=1))
    graph_html = fig.to_html(full_html=False)
    return graph_html


@superadmin_required(login_url="/")
def analytics_dashboard(request):
    context = {}
    context["page_visit_data"] = PageVisit.get_page_visit_data()
    context["registration_data"] = User.get_registration_data()
    context["most_visited_pages"] = (
        PageVisit.objects.values("page")
        .annotate(visit_count=Count("id"))
        .order_by("-visit_count")[:4]
    )

    context["graph_html"] = get_hourly_visits_graph()

    return render(request, "analytics/index.html", context)
