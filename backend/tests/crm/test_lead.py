import pytest

from apps.crm.models import Deal, Lead


@pytest.mark.django_db
def test_convert_lead_creates_deal(auth_client, organization, pipeline, user):
    lead = Lead.objects.create(
        organization=organization, title="Lead A", owner=user,
    )
    resp = auth_client.post(
        f"/api/v1/leads/{lead.id}/convert/",
        {"pipeline_id": str(pipeline.id)},
        format="json",
    )
    assert resp.status_code == 200, resp.content
    deal = Deal.objects.get(lead=lead)
    assert deal.title == "Lead A"
    lead.refresh_from_db()
    assert lead.status == Lead.Status.QUALIFIED


@pytest.mark.django_db
def test_cannot_convert_twice(auth_client, organization, pipeline, user):
    lead = Lead.objects.create(
        organization=organization, title="L", owner=user)
    auth_client.post(
        f"/api/v1/leads/{lead.id}/convert/",
        {"pipeline_id": str(pipeline.id)},
        format="json",
    )
    resp = auth_client.post(
        f"/api/v1/leads/{lead.id}/convert/",
        {"pipeline_id": str(pipeline.id)},
        format="json",
    )
    assert resp.status_code == 400
