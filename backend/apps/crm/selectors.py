from django.db.models import Q

from .models import Company, Contact, Deal, Lead, Pipeline


def list_companies(*, organization, params):
    qs = Company.objects.filter(
        organization=organization).select_related("owner")

    if search := params.get("search"):
        qs = qs.filter(
            Q(name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
        )
    if industry := params.get("industry"):
        qs = qs.filter(industry=industry)
    if owner := params.get("owner"):
        qs = qs.filter(owner_id=owner)

    return qs.order_by("name")


def list_contacts(*, organization, params):
    qs = Contact.objects.filter(
        organization=organization).select_related("company", "owner")

    if search := params.get("search"):
        qs = qs.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
        )
    if company := params.get("company"):
        qs = qs.filter(company_id=company)
    if owner := params.get("owner"):
        qs = qs.filter(owner_id=owner)

    return qs.order_by("first_name", "last_name")


def list_pipelines(*, organization, params):
    qs = Pipeline.objects.filter(
        organization=organization).prefetch_related("stages")

    if search := params.get("search"):
        qs = qs.filter(name__icontains=search)

    return qs.order_by("-is_default", "name")


def get_pipeline_with_stages(*, organization, pipeline_id):
    return (
        Pipeline.objects.filter(organization=organization, id=pipeline_id)
        .prefetch_related("stages")
        .first()
    )


def list_leads(*, organization, params):
    qs = Lead.objects.filter(organization=organization).select_related(
        "company", "contact", "owner"
    )

    if search := params.get("search"):
        qs = qs.filter(
            Q(title__icontains=search)
            | Q(company__name__icontains=search)
            | Q(contact__email__icontains=search)
        )
    if status := params.get("status"):
        qs = qs.filter(status=status)
    if source := params.get("source"):
        qs = qs.filter(source=source)
    if owner := params.get("owner"):
        qs = qs.filter(owner_id=owner)

    return qs.order_by("-created_at")


def list_deals(*, organization, params):
    qs = Deal.objects.filter(organization=organization).select_related(
        "company", "contact", "pipeline", "stage", "owner"
    )

    if search := params.get("search"):
        qs = qs.filter(
            Q(title__icontains=search) | Q(company__name__icontains=search)
        )
    if pipeline := params.get("pipeline"):
        qs = qs.filter(pipeline_id=pipeline)
    if stage := params.get("stage"):
        qs = qs.filter(stage_id=stage)
    if status := params.get("status"):
        qs = qs.filter(status=status)
    if owner := params.get("owner"):
        qs = qs.filter(owner_id=owner)

    return qs.order_by("order", "-created_at")


def kanban_board(*, organization, pipeline_id):
    """Return {pipeline, stages: [{..., deals: [...]}]} ready for Kanban UI."""
    pipeline = get_pipeline_with_stages(
        organization=organization, pipeline_id=pipeline_id)
    if not pipeline:
        return None

    stages = list(pipeline.stages.all())
    deals = (
        Deal.objects.filter(organization=organization, pipeline=pipeline)
        .select_related("company", "contact", "owner")
        .order_by("order", "-created_at")
    )

    by_stage = {}
    for d in deals:
        by_stage.setdefault(d.stage_id, []).append(d)

    return {
        "pipeline": pipeline,
        "stages": [
            {
                "id": str(s.id),
                "name": s.name,
                "order": s.order,
                "color": s.color,
                "is_won": s.is_won,
                "is_lost": s.is_lost,
                "deals": by_stage.get(s.id, []),
            }
            for s in stages
        ],
    }
