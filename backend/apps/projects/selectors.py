from django.db.models import Q

from .models import Invoice, Project


def list_projects(*, organization, params):
    qs = Project.objects.filter(organization=organization).select_related(
        "client_company", "owner", "deal"
    )

    if search := params.get("search"):
        qs = qs.filter(
            Q(name__icontains=search)
            | Q(client_company__name__icontains=search)
        )
    if status := params.get("status"):
        qs = qs.filter(status=status)
    if client := params.get("client"):
        qs = qs.filter(client_company_id=client)
    if owner := params.get("owner"):
        qs = qs.filter(owner_id=owner)

    return qs


def list_invoices(*, organization, params):
    qs = Invoice.objects.filter(
        organization=organization).select_related("project")

    if search := params.get("search"):
        qs = qs.filter(
            Q(number__icontains=search) | Q(project__name__icontains=search)
        )
    if status := params.get("status"):
        qs = qs.filter(status=status)
    if project := params.get("project"):
        qs = qs.filter(project_id=project)

    return qs
