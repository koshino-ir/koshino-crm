import pytest

from apps.accounts.models import Membership, Organization


@pytest.mark.django_db
def test_list_my_organizations(auth_client, organization):
    resp = auth_client.get("/api/v1/organizations/")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) == 1
    assert data[0]["id"] == str(organization.id)


@pytest.mark.django_db
def test_members_can_list_members(auth_client, organization, user):
    resp = auth_client.get(f"/api/v1/organizations/{organization.id}/members/")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 1


@pytest.mark.django_db
def test_only_owner_can_delete_org(auth_client, organization):
    resp = auth_client.delete(f"/api/v1/organizations/{organization.id}/")
    assert resp.status_code == 204
    assert Organization.objects.filter(id=organization.id).count() == 0
