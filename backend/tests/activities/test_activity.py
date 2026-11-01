import pytest
from django.utils import timezone

from apps.activities.models import Activity
from apps.crm.models import Deal


@pytest.mark.django_db
def test_create_activity(auth_client, organization, company, pipeline, user):
    deal = Deal.objects.create(
        organization=organization, company=company,
        pipeline=pipeline, stage=pipeline.stages.first(),
        title="D", owner=user,
    )
    resp = auth_client.post(
        "/api/v1/activities/",
        {
            "type": "call",
            "subject": "Intro call",
            "occurred_at": timezone.now().isoformat(),
            "deal_id": str(deal.id),
        },
        format="json",
    )
    assert resp.status_code == 201, resp.content
    assert Activity.objects.filter(subject="Intro call").exists()


@pytest.mark.django_db
def test_activity_requires_exactly_one_target(
    auth_client, organization, company, pipeline, user
):
    deal = Deal.objects.create(
        organization=organization, company=company,
        pipeline=pipeline, stage=pipeline.stages.first(),
        title="D", owner=user,
    )
    resp = auth_client.post(
        "/api/v1/activities/",
        {
            "type": "note",
            "subject": "ambiguous",
            "occurred_at": timezone.now().isoformat(),
            "deal_id": str(deal.id),
            "company_id": str(company.id),
        },
        format="json",
    )
    assert resp.status_code == 400
