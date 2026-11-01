from typing import Any, Optional

from rest_framework.response import Response
from rest_framework import status as drf_status


class APIResponse(Response):
    """Envelope response used across the entire API."""

    def __init__(
        self,
        data: Any = None,
        *,
        success: bool = True,
        message: str = "",
        errors: Optional[Any] = None,
        meta: Optional[dict] = None,
        status: int = drf_status.HTTP_200_OK,
        headers: Optional[dict] = None,
        **kwargs,
    ):
        payload = {
            "success": success,
            "data": data,
            "message": message,
            "errors": errors,
            "meta": meta,
        }
        super().__init__(payload, status=status, headers=headers, **kwargs)


def ok(data=None, *, message="OK", meta=None, status=200):
    return APIResponse(data=data, message=message, meta=meta, status=status)


def created(data=None, *, message="Created", meta=None):
    return APIResponse(data=data, message=message, meta=meta, status=201)


def no_content(message="Deleted"):
    return APIResponse(data=None, message=message, status=204)


def error(message="Error", *, errors=None, status=400):
    return APIResponse(success=False, data=None, message=message, errors=errors, status=status)
