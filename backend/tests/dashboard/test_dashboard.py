import pytest

from apps.crm.models import Deal


@pytest.mark.django_db
def test_kpi_stats(auth_client, organization, company, pipeline, user):
    Deal.objects.create(
        organization=organization, company=company,
        pipeline=pipeline, stage=pipeline.stages.first(),
        title="Open one", owner=user, amount="1000.00",
    )
    resp = auth_client.get("/api/v1/dashboard/stats/")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["open_deals_count"] == 1
    assert float(data["open_deals_value"]) == 1000.0


@pytest.mark.django_db
def test_funnel_returns_stages(auth_client, organization, company, pipeline, user):
    Deal.objects.create(
        organization=organization, company=company,
        pipeline=pipeline, stage=pipeline.stages.first(),
        title="X", owner=user,
    )
    resp = auth_client.get("/api/v1/dashboard/funnel/")
    assert resp.status_code == 200
    body = resp.json()["data"]
    assert len(body) >= 1
    assert body[0]["count"] >= 1


@pytest.mark.django_db
def test_global_search(auth_client, organization, company):
    resp = auth_client.get("/api/v1/search/?q=acme")
    assert resp.status_code == 200
    results = resp.json()["data"]["results"]
    assert any(r["type"] == "company" and "Acme" in r["title"]
               for r in results)


@pytest.mark.django_db
def test_audit_log_created_on_deal(auth_client, organization, company, pipeline, user):
    Deal.objects.create(
        organization=organization, company=company,
        pipeline=pipeline, stage=pipeline.stages.first(),
        title="Auditable", owner=user,
    )
    resp = auth_client.get("/api/v1/audit-logs/?entity_type=deal")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert any(item["entity_type"] == "deal" for item in data)
