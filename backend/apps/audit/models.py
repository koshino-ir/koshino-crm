from django.db import models

from apps.common.models import OrganizationScopedModel


class AuditLog(OrganizationScopedModel):
    class Action(models.TextChoices):
        CREATE = "create", "Create"
        UPDATE = "update", "Update"
        DELETE = "delete", "Delete"

    user = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="audit_logs",
    )
    action = models.CharField(max_length=16, choices=Action.choices)
    entity_type = models.CharField(max_length=64)
    entity_id = models.CharField(max_length=64)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)

    class Meta:
        db_table = "audit_audit_log"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["organization", "-created_at"]),
            models.Index(fields=["entity_type", "entity_id"]),
        ]

    def __str__(self):
        return f"{self.action} {self.entity_type}#{self.entity_id}"
