import pytest
from rest_framework.test import APIClient

from apps.accounts.models import Membership, Organization, User
from apps.crm.models import Company, Pipeline, Stage


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(email="owner@example.com", password="secure-pass-123")


@pytest.fixture
def organization(db, user):
    org = Organization.objects.create(name="Test Org")
    Membership.objects.create(
        user=user, organization=org, role=Membership.Role.OWNER)
    return org


@pytest.fixture
def auth_client(api_client, user):
    resp = api_client.post(
        "/api/v1/auth/login/",
        {"email": user.email, "password": "secure-pass-123"},
        format="json",
    )
    assert resp.status_code == 200, resp.content
    return api_client


# ---- CRM fixtures (used across all test modules) ----

@pytest.fixture
def pipeline(db, organization):
    p = Pipeline.objects.create(organization=organization, name="Sales")
    Stage.objects.create(organization=organization,
                         pipeline=p, name="Qualify", order=0)
    Stage.objects.create(organization=organization,
                         pipeline=p, name="Won", order=1, is_won=True)
    Stage.objects.create(organization=organization,
                         pipeline=p, name="Lost", order=2, is_lost=True)
    return p


@pytest.fixture
def company(db, organization, user):
    return Company.objects.create(organization=organization, name="Acme", owner=user)
