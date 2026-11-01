import pytest

from apps.crm.models import Deal


@pytest.mark.django_db
def test_create_deal_places_in_first_stage(
    auth_client, organization, company, pipeline, user
):
    first_stage = pipeline.stages.first()
    resp = auth_client.post(
        "/api/v1/deals/",
        {
            "title": "Big deal",
            "company_id": str(company.id),
            "pipeline_id": str(pipeline.id),
            "amount": "5000.00",
        },
        format="json",
    )
    assert resp.status_code == 201, resp.content
    deal = Deal.objects.get(title="Big deal")
    assert deal.stage_id == first_stage.id
    assert deal.owner_id == user.id


@pytest.mark.django_db
def test_move_deal_updates_stage_and_status(
    auth_client, organization, company, pipeline, user
):
    first, won = list(pipeline.stages.all()[:2])
    deal = Deal.objects.create(
        organization=organization, company=company,
        pipeline=pipeline, stage=first, title="D1", owner=user,
    )
    resp = auth_client.patch(
        f"/api/v1/deals/{deal.id}/move/",
        {"stage_id": str(won.id)},
        format="json",
    )
    assert resp.status_code == 200
    deal.refresh_from_db()
    assert deal.stage_id == won.id
    assert deal.status == Deal.Status.WON


@pytest.mark.django_db
def test_move_deal_rejects_cross_pipeline_stage(
    auth_client, organization, company, pipeline, user
):
    other = type(pipeline).objects.create(
        organization=organization, name="Other")
    other_stage = other.stages.create(
        organization=organization, name="Only", order=0
    )
    deal = Deal.objects.create(
        organization=organization, company=company,
        pipeline=pipeline, stage=pipeline.stages.first(), title="D2", owner=user,
    )
    resp = auth_client.patch(
        f"/api/v1/deals/{deal.id}/move/",
        {"stage_id": str(other_stage.id)},
        format="json",
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_kanban_groups_by_stage(
    auth_client, organization, company, pipeline, user
):
    stage = pipeline.stages.first()
    Deal.objects.create(
        organization=organization, company=company,
        pipeline=pipeline, stage=stage, title="K1", owner=user,
    )
    Deal.objects.create(
        organization=organization, company=company,
        pipeline=pipeline, stage=stage, title="K2", owner=user,
    )
    resp = auth_client.get(f"/api/v1/deals/kanban/?pipeline={pipeline.id}")
    assert resp.status_code == 200
    body = resp.json()["data"]
    assert body["pipeline"]["id"] == str(pipeline.id)
    first_col = body["stages"][0]
    assert len(first_col["deals"]) == 2
