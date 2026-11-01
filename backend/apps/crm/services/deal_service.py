from django.db import transaction
from django.db.models import Max

from apps.crm.models import Company, Deal


@transaction.atomic
def create_deal(*, organization, serializer):
    """
    Create a deal and place it at the end of its stage.

    `serializer.validated_data` already holds resolved model instances under
    `pipeline_id`, `stage_id`, and `company_id` (via `validate_*_id` methods).
    We compute `stage` and `order`, then delegate actual creation to the
    serializer so its `create()` method can pop the FK fields correctly.
    """
    data = serializer.validated_data
    # Pipeline instance (resolved in serializer)
    pipeline = data["pipeline_id"]

    stage = data.get("stage_id")
    if stage is None:
        stage = pipeline.stages.order_by("order").first()
    if stage is None:
        raise ValueError("Pipeline has no stages.")
    if stage.pipeline_id != pipeline.id:
        raise ValueError("Stage does not belong to the given pipeline.")

    # Ensure serializer.create() sees the resolved stage
    data["stage_id"] = stage

    max_order = (
        Deal.objects
        .filter(organization=organization, pipeline=pipeline, stage=stage)
        .aggregate(m=Max("order"))["m"]
    )
    next_order = (max_order + 1) if max_order is not None else 0

    return serializer.save(
        organization=organization,
        owner=serializer.context["request"].user,
        order=next_order,
    )


@transaction.atomic
def move_deal(*, deal, stage, order=None):
    """Move a deal to another stage (Kanban drag & drop)."""
    if stage.pipeline_id != deal.pipeline_id:
        raise ValueError("Target stage belongs to a different pipeline.")

    if order is None:
        max_order = (
            Deal.objects
            .filter(organization=deal.organization, pipeline=deal.pipeline, stage=stage)
            .exclude(pk=deal.pk)
            .aggregate(m=Max("order"))["m"]
        )
        order = (max_order + 1) if max_order is not None else 0

    deal.stage = stage
    deal.order = order

    if stage.is_won:
        deal.status = Deal.Status.WON
    elif stage.is_lost:
        deal.status = Deal.Status.LOST
    else:
        deal.status = Deal.Status.OPEN

    deal.save(update_fields=["stage", "order", "status", "updated_at"])
    return deal


@transaction.atomic
def convert_lead_to_deal(*, lead, pipeline, stage=None, owner=None):
    """Create a Deal from a qualified Lead, auto-provisioning a Company if needed."""
    if lead.deals.exists():
        raise ValueError("Lead has already been converted to a deal.")

    target_stage = stage or pipeline.stages.order_by("order").first()
    if not target_stage:
        raise ValueError("Pipeline has no stages.")
    if target_stage.pipeline_id != pipeline.id:
        raise ValueError("Stage does not belong to the pipeline.")

    company = lead.company
    if not company:
        company = Company.objects.create(
            organization=lead.organization,
            name=lead.title,
            owner=owner or lead.owner,
        )

    max_order = (
        Deal.objects
        .filter(organization=lead.organization, pipeline=pipeline, stage=target_stage)
        .aggregate(m=Max("order"))["m"]
    )

    deal = Deal.objects.create(
        organization=lead.organization,
        lead=lead,
        company=company,
        contact=lead.contact,
        pipeline=pipeline,
        stage=target_stage,
        title=lead.title,
        owner=owner or lead.owner,
        order=(max_order + 1) if max_order is not None else 0,
    )

    lead.status = Lead.Status.QUALIFIED
    lead.save(update_fields=["status", "updated_at"])

    return deal


from apps.crm.models import Lead  # noqa: E402  (avoid circular)
