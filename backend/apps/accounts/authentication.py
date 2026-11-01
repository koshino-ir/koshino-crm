from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class JWTCookieAuthentication(JWTAuthentication):
    """
    Authenticates via JWT stored in httpOnly cookie.
    Enforces CSRF on unsafe methods since cookies are used.
    """

    def authenticate(self, request):
        raw_token = request.COOKIES.get("access_token")
        if not raw_token:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except TokenError as exc:
            raise InvalidToken({"detail": str(exc)}) from exc

        if request.method not in ("GET", "HEAD", "OPTIONS", "TRACE"):
            self._enforce_csrf(request)

        return self.get_user(validated_token), validated_token

    def _enforce_csrf(self, request):
        check = authentication.CSRFCheck(lambda req: None)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(
                _("CSRF Failed: %(reason)s") % {"reason": reason}
            )
