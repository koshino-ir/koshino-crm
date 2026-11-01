from django.urls import path

from .views import FunnelView, KPIStatsView, RecentActivitiesView, RevenueView

app_name = "dashboard"

urlpatterns = [
    path("dashboard/stats/", KPIStatsView.as_view(), name="stats"),
    path("dashboard/funnel/", FunnelView.as_view(), name="funnel"),
    path("dashboard/revenue/", RevenueView.as_view(), name="revenue"),
    path("dashboard/recent-activities/",
         RecentActivitiesView.as_view(), name="recent-activities"),
]
