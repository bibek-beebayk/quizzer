from django.shortcuts import render
from apps.analytics.models import PageVisit, WebsiteAnalytics
from core.libs.decorators import superadmin_required
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncHour
import pandas as pd
import plotly.express as px

User = get_user_model()

default_layout_config = {
    "height": 300,
    "autosize": True,
    "showlegend": False,
    "margin": {"t": 50, "b": 0, "l": 60, "r": 20},
    "dragmode": False,
    "xaxis": {"showgrid": True, "ticklen": 1, "tickangle": 0, "title_standoff": 20},
    "yaxis": {"showgrid": True},
    "modebar": {"orientation": "h"},
}


def get_daily_traffic_graph():
    analytics = WebsiteAnalytics()
    daily_traffic_data = analytics.daily_traffic(days=7)
    df = pd.DataFrame(daily_traffic_data)
    fig = px.line(
        df,
        x="date",
        y="visits",
        title="Daily Traffic",
        markers=True,
        labels={"date": "Date", "visits": "Number of page visits"},
        line_shape="spline",
    )
    fig.update_layout(**default_layout_config)
    graph_html = fig.to_html(full_html=False)
    return graph_html


def get_hourly_distribution_graph():
    analytics = WebsiteAnalytics()
    hourly_distribution_data = analytics.hourly_distribution()
    df = pd.DataFrame(hourly_distribution_data)
    fig = px.line(
        df,
        x="hour",
        y="visits",
        title="Hourly Distribution",
        markers=True,
        labels={"hour": "Hour", "visits": "Number of page visits"},
        line_shape="spline",
    )
    fig.update_layout(
        **default_layout_config,
    )
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

    context["daily_traffic"] = get_daily_traffic_graph()
    context["hourly_distribution"] = get_hourly_distribution_graph()
    
    analytics = WebsiteAnalytics()
    print(analytics.bounce_rate())

    return render(request, "analytics/index.html", context)
