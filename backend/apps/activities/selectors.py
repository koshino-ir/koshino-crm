from django.db.models import Q

from .models import Activity, Task


def list_activities(*, organization, params):
    qs = Activity.objects.filter(organization=organization).select_related(
        "created_by", "deal", "lead", "contact", "company"
    )

    if search := params.get("search"):
        qs = qs.filter(Q(subject__icontains=search) |
                       Q(description__icontains=search))
    if type_ := params.get("type"):
        qs = qs.filter(type=type_)
    if deal := params.get("deal"):
        qs = qs.filter(deal_id=deal)
    if lead := params.get("lead"):
        qs = qs.filter(lead_id=lead)
    if company := params.get("company"):
        qs = qs.filter(company_id=company)
    if date_from := params.get("date_from"):
        qs = qs.filter(occurred_at__date__gte=date_from)
    if date_to := params.get("date_to"):
        qs = qs.filter(occurred_at__date__lte=date_to)

    return qs


def list_tasks(*, organization, params):
    qs = Task.objects.filter(organization=organization).select_related(
        "assigned_to", "deal", "lead"
    )

    if search := params.get("search"):
        qs = qs.filter(Q(title__icontains=search) |
                       Q(description__icontains=search))
    if status := params.get("status"):
        qs = qs.filter(status=status)
    if priority := params.get("priority"):
        qs = qs.filter(priority=priority)
    if assigned_to := params.get("assigned_to"):
        qs = qs.filter(assigned_to_id=assigned_to)
    if due_before := params.get("due_before"):
        qs = qs.filter(due_date__lte=due_before)
    if deal := params.get("deal"):
        qs = qs.filter(deal_id=deal)

    return qs
