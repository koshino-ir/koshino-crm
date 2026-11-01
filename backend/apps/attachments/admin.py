from django.contrib import admin

from .models import Attachment


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("original_name", "size", "mime_type",
                    "uploaded_by", "created_at")
    search_fields = ("original_name",)
