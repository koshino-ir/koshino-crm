from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


def issue_tokens_for_user(user):
    """Return (access_token_str, refresh_token_str) for a user."""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


def set_auth_cookies(response, access_token, refresh_token):
    response.set_cookie(
        key=settings.AUTH_COOKIE_ACCESS,
        value=access_token,
        max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path="/",
    )
    response.set_cookie(
        key=settings.AUTH_COOKIE_REFRESH,
        value=refresh_token,
        max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path="/",
    )
    return response


def clear_auth_cookies(response):
    response.delete_cookie(settings.AUTH_COOKIE_ACCESS, path="/")
    response.delete_cookie(settings.AUTH_COOKIE_REFRESH, path="/")
    return response
