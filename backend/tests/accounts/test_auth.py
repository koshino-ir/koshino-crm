import pytest

from apps.accounts.models import User


@pytest.mark.django_db
def test_register_creates_user_and_org(api_client):
    resp = api_client.post(
        "/api/v1/auth/register/",
        {
            "email": "new@example.com",
            "password": "Strong-Pass-123",
            "organization_name": "New Co",
        },
        format="json",
    )
    assert resp.status_code == 201, resp.content
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["email"] == "new@example.com"
    assert len(body["data"]["organizations"]) == 1
    assert body["data"]["organizations"][0]["role"] == "owner"
    assert "access_token" in resp.cookies
    assert "refresh_token" in resp.cookies


@pytest.mark.django_db
def test_login_sets_cookies_and_returns_user(api_client, user):
    resp = api_client.post(
        "/api/v1/auth/login/",
        {"email": user.email, "password": "secure-pass-123"},
        format="json",
    )
    assert resp.status_code == 200
    assert "access_token" in resp.cookies


@pytest.mark.django_db
def test_login_invalid_credentials(api_client, user):
    resp = api_client.post(
        "/api/v1/auth/login/",
        {"email": user.email, "password": "wrong"},
        format="json",
    )
    assert resp.status_code == 400
    assert resp.json()["success"] is False


@pytest.mark.django_db
def test_me_requires_auth(api_client):
    resp = api_client.get("/api/v1/auth/me/")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_me_returns_user_with_cookie_auth(auth_client, user):
    resp = auth_client.get("/api/v1/auth/me/")
    assert resp.status_code == 200
    assert resp.json()["data"]["email"] == user.email


@pytest.mark.django_db
def test_logout_clears_cookies(auth_client):
    resp = auth_client.post("/api/v1/auth/logout/")
    assert resp.status_code == 200
    # Cookie deletion is indicated by empty value with past expiry
    assert resp.cookies["access_token"].value == ""
