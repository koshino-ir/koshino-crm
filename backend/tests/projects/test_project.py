import pytest

from apps.projects.models import Project


@pytest.mark.django_db
def test_create_project(auth_client, organization, company, user):
    resp = auth_client.post(
        "/api/v1/projects/",
        {
            "name": "Website Revamp",
            "client_company_id": str(company.id),
            "budget": "5000.00",
            "status": "active",
        },
        format="json",
    )
    assert resp.status_code == 201, resp.content
    assert Project.objects.filter(name="Website Revamp").exists()
    p = Project.objects.get(name="Website Revamp")
    assert p.owner_id == user.id
    assert p.organization_id == organization.id


@pytest.mark.django_db
def test_project_invalid_dates(auth_client, organization, company):
    resp = auth_client.post(
        "/api/v1/projects/",
        {
            "name": "Bad dates",
            "client_company_id": str(company.id),
            "start_date": "2026-06-01",
            "end_date": "2026-05-01",
        },
        format="json",
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_tenant_isolation(auth_client, organization, company, user):
    from apps.accounts.models import Membership, Organization as Org
    from apps.projects.models import Project as P
    other_org = Org.objects.create(name="Other")
    Membership.objects.create(
        user=user, organization=other_org, role=Membership.Role.OWNER)
    other_company = type(company).objects.create(
        organization=other_org, name="OtherCo")
    P.objects.create(organization=other_org, name="Leaky",
                     client_company=other_company)

    resp = auth_client.get("/api/v1/projects/")
    names = [p["name"] for p in resp.json()["data"]]
    assert "Leaky" not in names
