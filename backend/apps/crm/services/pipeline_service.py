from django.db import transaction

from apps.crm.models import Pipeline, Stage

DEFAULT_STAGES = [
    # (name, order, color, is_won, is_lost)
    ("Qualified", 0, "#6366F1", False, False),
    ("Proposal", 1, "#0EA5E9", False, False),
    ("Negotiation", 2, "#F59E0B", False, False),
    ("Won", 3, "#10B981", True, False),
    ("Lost", 4, "#F43F5E", False, True),
]


@transaction.atomic
def ensure_default_pipeline(*, organization) -> Pipeline:
    """
    Return the org's default pipeline. If none exists, create one with
    the standard sales stages. Idempotent.
    """
    existing = (
        Pipeline.objects
        .filter(organization=organization)
        .prefetch_related("stages")
        .order_by("-is_default", "created_at")
        .first()
    )
    if existing:
        return existing

    pipeline = Pipeline.objects.create(
        organization=organization, name="Sales Pipeline", is_default=True
    )
    Stage.objects.bulk_create([
        Stage(
            organization=organization,
            pipeline=pipeline,
            name=name,
            order=order,
            color=color,
            is_won=is_won,
            is_lost=is_lost,
        )
        for name, order, color, is_won, is_lost in DEFAULT_STAGES
    ])
    return pipeline
