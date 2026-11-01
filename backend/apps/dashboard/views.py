from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.activities.models import Activity
from apps.common.mixins import OrgScopedViewMixin
from apps.common.responses import ok

from .selectors import funnel, kpi_stats, revenue_by_month


class KPIStatsView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return ok(data=kpi_stats(organization=request.organization))


class FunnelView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return ok(data=funnel(organization=request.organization))


class RevenueView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            months = min(int(request.query_params.get("months", 6)), 24)
        except ValueError:
            months = 6
        return ok(data=revenue_by_month(organization=request.organization, months=months))


class RecentActivitiesView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = (
            Activity.objects
            .filter(organization=request.organization)
            .select_related("created_by")
            .order_by("-occurred_at")[:10]
        )
        from apps.activities.serializers import ActivitySerializer
        return ok(data=ActivitySerializer(qs, many=True).data)
