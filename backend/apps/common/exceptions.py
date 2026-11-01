import logging

from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from .responses import APIResponse

logger = logging.getLogger(__name__)


def _flatten_errors(detail):
    """Recursively flatten DRF error detail into a plain dict/list."""
    if isinstance(detail, dict):
        return {k: _flatten_errors(v) for k, v in detail.items()}
    if isinstance(detail, list):
        return [_flatten_errors(v) for v in detail]
    return str(detail)


def _first_error_message(errors) -> str:
    """Extract the first human-readable string from a flattened errors structure."""
    if isinstance(errors, str):
        return errors
    if isinstance(errors, list):
        for item in errors:
            msg = _first_error_message(item)
            if msg:
                return msg
        return ""
    if isinstance(errors, dict):
        # `non_field_errors` and `detail` come first (they're the most general)
        for preferred_key in ("detail", "non_field_errors"):
            if preferred_key in errors:
                msg = _first_error_message(errors[preferred_key])
                if msg:
                    return msg
        for value in errors.values():
            msg = _first_error_message(value)
            if msg:
                return msg
    return ""


def custom_exception_handler(exc, context):
    # Normalize Django ValidationError into DRF's
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(
            exc.message_dict if hasattr(exc, "message_dict") else exc.messages
        )

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    # JWT-specific errors
    if isinstance(exc, (InvalidToken, TokenError)):
        return APIResponse(
            success=False,
            message="Authentication credentials are invalid or expired.",
            errors=_flatten_errors(exc.detail),
            status=status.HTTP_401_UNAUTHORIZED,
        )

    response = drf_exception_handler(exc, context)
    if response is None:
        logger.exception("Unhandled exception: %s", exc)
        return APIResponse(
            success=False,
            message="Internal server error.",
            errors=None,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Build errors & message
    errors = _flatten_errors(response.data)

    # If the backend produced a top-level "detail", use it as message.
    if isinstance(errors, dict) and "detail" in errors:
        message = _first_error_message(errors["detail"]) or "Request failed."
        # Drop the "detail" from errors to avoid duplication
        errors = {k: v for k, v in errors.items() if k != "detail"} or None
    else:
        # No "detail" — try to get the first field error so message is useful
        message = _first_error_message(errors) or "Request failed."

    return APIResponse(
        success=False,
        message=message,
        errors=errors,
        status=response.status_code,
    )
