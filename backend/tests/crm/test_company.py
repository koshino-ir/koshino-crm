import pytest

from apps.crm.models import Company


@pytest.mark.django_db
def test_list_companies(auth_client, organization, company):
    resp = auth_client.get("/api/v1/companies/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert len(body["data"]) == 1
    assert body["data"][0]["name"] == "Acme"


@pytest.mark.django_db
def test_create_company_sets_owner_and_org(auth_client, organization, user):
    resp = auth_client.post(
        "/api/v1/companies/",
        {"name": "Beta Ltd", "industry": "Finance"},
        format="json",
        HTTP_X_CSRFTOKEN="dummy",  # CSRF check on the test client is disabled
    )
    assert resp.status_code == 201, resp.content
    assert resp.json()["data"]["owner"]["id"] == str(user.id)
    assert Company.objects.filter(
        name="Beta Ltd", organization=organization).exists()


@pytest.mark.django_db
def test_search_companies(auth_client, organization, company):
    Company.objects.create(organization=organization, name="Other Inc")
    resp = auth_client.get("/api/v1/companies/?search=acme")
    assert len(resp.json()["data"]) == 1


@pytest.mark.django_db
def test_tenant_isolation(auth_client, organization, company, user):
    from apps.accounts.models import Membership, Organization
    from apps.crm.models import Company as C
    other_org = Organization.objects.create(name="Other")
    Membership.objects.create(
        user=user, organization=other_org, role=Membership.Role.OWNER)
    C.objects.create(organization=other_org, name="Leaky")
    resp = auth_client.get("/api/v1/companies/")
    names = [c["name"] for c in resp.json()["data"]]
    assert "Leaky" not in names
