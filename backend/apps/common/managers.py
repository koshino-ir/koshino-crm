from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)

    def soft_delete(self):
        return self.update(deleted_at=timezone.now())

    def restore(self):
        return self.update(deleted_at=None)


class ActiveManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """Default manager — returns only rows that haven't been soft-deleted."""

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class AllObjectsManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """Includes soft-deleted rows (for admin, audit, restore)."""
