from datetime import timedelta

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from apps.activities.models import Task
from apps.crm.models import Company, Deal, Lead


def kpi_stats(*, organization):
    """Cards for the dashboard top row."""
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    open_deals = Deal.objects.filter(
        organization=organization, status=Deal.Status.OPEN
    )
    won_this_month = Deal.objects.filter(
        organization=organization,
        status=Deal.Status.WON,
        updated_at__gte=month_start,
    )

    return {
        "open_deals_count": open_deals.count(),
        "open_deals_value": open_deals.aggregate(
            total=Sum("amount")
        )["total"] or 0,
        "won_deals_count": won_this_month.count(),
        "won_deals_value": won_this_month.aggregate(
            total=Sum("amount")
        )["total"] or 0,
        "companies_count": Company.objects.filter(organization=organization).count(),
        "leads_count": Lead.objects.filter(
            organization=organization, status=Lead.Status.NEW
        ).count(),
        "tasks_open_count": Task.objects.filter(
            organization=organization
        ).exclude(status=Task.Status.DONE).count(),
        "tasks_overdue_count": Task.objects.filter(
            organization=organization,
            due_date__lt=now.date(),
        ).exclude(status=Task.Status.DONE).count(),
    }


def funnel(*, organization):
    """Deal counts per pipeline stage."""
    rows = (
        Deal.objects
        .filter(organization=organization, status=Deal.Status.OPEN)
        .values("stage_id", "stage__name", "stage__order", "stage__color")
        .annotate(count=Count("id"), total=Sum("amount"))
        .order_by("stage__order")
    )
    return [
        {
            "stage_id": str(r["stage_id"]),
            "name": r["stage__name"],
            "color": r["stage__color"],
            "count": r["count"],
            "total": r["total"] or 0,
        }
        for r in rows
    ]


def revenue_by_month(*, organization, months=6):
    """Won deals summed per month for the last `months` months."""
    since = timezone.now() - timedelta(days=30 * months)
    rows = (
        Deal.objects
        .filter(
            organization=organization,
            status=Deal.Status.WON,
            updated_at__gte=since,
        )
        .annotate(month=TruncMonth("updated_at"))
        .values("month")
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("month")
    )
    return [
        {
            "month": r["month"].strftime("%Y-%m") if r["month"] else None,
            "total": r["total"] or 0,
            "count": r["count"],
        }
        for r in rows
    ]
