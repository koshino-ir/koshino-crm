import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.accounts.services.oauth_service import (
    build_google_auth_url, exchange_code_for_userinfo,
    get_or_create_user_from_google, verify_state,
)
from apps.accounts.services.token_service import issue_tokens_for_user, set_auth_cookies
from apps.common.responses import APIResponse, ok

logger = logging.getLogger(__name__)


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "oauth"

    def get(self, request):
        redirect_to = request.query_params.get(
            "redirect", settings.FRONTEND_URL)
        if not settings.GOOGLE_CLIENT_ID:
            return APIResponse(
                success=False, message="Google OAuth not configured.", status=503,
            )
        url = build_google_auth_url(redirect_to)
        return ok(data={"url": url})


class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_scope = "oauth"

    def get(self, request):
        code = request.query_params.get("code")
        state = request.query_params.get("state", "")
        error = request.query_params.get("error")

        if error or not code:
            return HttpResponseRedirect(f"{settings.FRONTEND_URL}/auth/callback?error=oauth_failed")

        try:
            redirect_to = verify_state(state)
        except Exception:
            return HttpResponseRedirect(f"{settings.FRONTEND_URL}/auth/callback?error=invalid_state")

        try:
            userinfo = exchange_code_for_userinfo(code)
            user = get_or_create_user_from_google(userinfo)
        except Exception:
            logger.exception("Google OAuth failed")
            return HttpResponseRedirect(f"{settings.FRONTEND_URL}/auth/callback?error=oauth_failed")

        access, refresh = issue_tokens_for_user(user)
        response = HttpResponseRedirect(
            f"{redirect_to}/auth/callback?success=true")
        set_auth_cookies(response, access, refresh)
        return response
