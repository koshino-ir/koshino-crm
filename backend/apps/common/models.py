import uuid

from django.db import models
from django.utils import timezone

from .managers import ActiveManager, AllObjectsManager


class BaseModel(models.Model):
    """Abstract base with UUID PK, audit timestamps, and soft delete."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = ActiveManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True
        ordering = ("-created_at",)

    def delete(self, using=None, keep_parents=False, *, hard=False):
        if hard:
            return super().delete(using=using, keep_parents=keep_parents)
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])
        return None

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at", "updated_at"])


class OrganizationScopedModel(BaseModel):
    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        db_index=True,
    )

    class Meta(BaseModel.Meta):
        abstract = True
