import os

from django.db import models

from apps.common.models import OrganizationScopedModel


def upload_to(instance, filename):
    return f"attachments/{instance.organization_id}/{instance.id}/{filename}"


class Attachment(OrganizationScopedModel):
    """
    A file attached to exactly one of: deal, company, project.
    """

    file = models.FileField(upload_to=upload_to, max_length=500)
    original_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100, blank=True)
    size = models.PositiveBigIntegerField(default=0)

    uploaded_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="uploaded_attachments",
    )

    deal = models.ForeignKey(
        "crm.Deal", on_delete=models.CASCADE, null=True, blank=True,
        related_name="attachments",
    )
    company = models.ForeignKey(
        "crm.Company", on_delete=models.CASCADE, null=True, blank=True,
        related_name="attachments",
    )
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, null=True, blank=True,
        related_name="attachments",
    )

    class Meta:
        db_table = "attachments_attachment"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["organization", "deal"]),
            models.Index(fields=["organization", "company"]),
            models.Index(fields=["organization", "project"]),
        ]

    def __str__(self):
        return self.original_name

    def delete(self, *args, **kwargs):
        """Delete underlying file when hard-deleting the model instance."""
        if kwargs.get("hard"):
            storage = self.file.storage
            if self.file and storage.exists(self.file.name):
                storage.delete(self.file.name)
        return super().delete(*args, **kwargs)
