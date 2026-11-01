import logging
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.core import signing
from django.db import transaction

from apps.accounts.models import Membership, Organization, User

logger = logging.getLogger(__name__)

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

_STATE_SALT = "google-oauth-state"


def build_google_auth_url(redirect_to: str) -> str:
    state = signing.dumps({"redirect_to": redirect_to}, salt=_STATE_SALT)
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "online",
        "prompt": "consent",
    }
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"


def verify_state(state: str, max_age: int = 600) -> str:
    data = signing.loads(state, salt=_STATE_SALT, max_age=max_age)
    return data.get("redirect_to") or settings.FRONTEND_URL


def exchange_code_for_userinfo(code: str) -> dict:
    token_resp = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
        timeout=10,
    )
    token_resp.raise_for_status()
    access_token = token_resp.json()["access_token"]

    userinfo_resp = requests.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    userinfo_resp.raise_for_status()
    return userinfo_resp.json()


@transaction.atomic
def get_or_create_user_from_google(userinfo: dict) -> User:
    email = userinfo["email"].lower()
    google_id = userinfo["sub"]

    user = User.objects.filter(google_id=google_id).first()
    if user:
        return user

    user = User.objects.filter(email=email).first()
    if user:
        user.google_id = google_id
        user.save(update_fields=["google_id", "updated_at"])
        return user

    user = User.objects.create_user(
        email=email,
        password=None,
        first_name=userinfo.get("given_name", ""),
        last_name=userinfo.get("family_name", ""),
        google_id=google_id,
    )
    user.set_unusable_password()
    user.save(update_fields=["password"])

    # Auto-provision a personal organization so the user can start immediately
    org = Organization.objects.create(
        name=f"{user.get_full_name()}'s Workspace")
    Membership.objects.create(
        user=user, organization=org, role=Membership.Role.OWNER)
    return user
