from django.conf import settings
from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = {
    "pdf", "png", "jpg", "jpeg", "gif", "webp", "svg",
    "doc", "docx", "xls", "xlsx", "ppt", "pptx",
    "txt", "csv", "zip",
}
MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def validate_upload(file_obj) -> None:
    """Raise ValidationError on unsupported extension or oversized file."""
    ext = file_obj.name.rsplit(
        ".", 1)[-1].lower() if "." in file_obj.name else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"File type '.{ext}' is not allowed. "
            f"Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}."
        )
    if file_obj.size > MAX_SIZE_BYTES:
        raise ValidationError(
            f"File is too large ({file_obj.size} bytes). "
            f"Maximum is {MAX_SIZE_BYTES // (1024 * 1024)} MB."
        )
