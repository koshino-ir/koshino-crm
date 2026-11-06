from django.conf import settings
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.accounts.serializers.auth import (
    LoginSerializer, MeSerializer, PasswordChangeSerializer, RegisterSerializer,
)
from apps.accounts.services.auth_service import register_user
from apps.accounts.services.token_service import (
    clear_auth_cookies, issue_tokens_for_user, set_auth_cookies,
)
from apps.common.responses import APIResponse, ok, created


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_scope = "auth"

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, org = register_user(**serializer.validated_data)

        access, refresh = issue_tokens_for_user(user)
        response = APIResponse(
            data=MeSerializer(user, context={"request": request}).data,
            message="Account created.",
            status=201,
        )
        set_auth_cookies(response, access, refresh)
        get_token(request)  # ensure CSRF cookie is set
        return response


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_scope = "auth"

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        access, refresh = issue_tokens_for_user(user)
        response = ok(
            data=MeSerializer(user, context={"request": request}).data,
            message="Logged in.",
        )
        set_auth_cookies(response, access, refresh)
        get_token(request)
        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        response = ok(message="Logged out.")
        return clear_auth_cookies(response)


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_scope = "auth"

    def post(self, request):
        raw_refresh = request.COOKIES.get(settings.AUTH_COOKIE_REFRESH)
        if not raw_refresh:
            return APIResponse(
                success=False, message="Refresh token missing.",
                status=401,
            )
        try:
            refresh = RefreshToken(raw_refresh)
            new_access = str(refresh.access_token)
            new_refresh = str(
                refresh) if not settings.SIMPLE_JWT["ROTATE_REFRESH_TOKENS"] else str(refresh)
        except TokenError:
            response = APIResponse(
                success=False, message="Refresh token invalid or expired.", status=401,
            )
            return clear_auth_cookies(response)

        response = ok(message="Token refreshed.")
        set_auth_cookies(response, new_access, new_refresh)
        return response


class MeView(APIView):
    def get(self, request):
        return ok(data=MeSerializer(request.user, context={"request": request}).data)

    def patch(self, request):
        serializer = MeSerializer(
            request.user, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ok(data=serializer.data, message="Profile updated.")


class PasswordChangeView(APIView):
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save(update_fields=["password", "updated_at"])
        return ok(message="Password changed.")
