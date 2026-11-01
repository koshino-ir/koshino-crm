from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.crm.models import Company, Deal

from .models import AuditLog


def _diff(instance):
    """Return tracked field values for the audit log. Kept small on purpose."""
    if isinstance(instance, Deal):
        return {
            "title": instance.title,
            "stage_id": str(instance.stage_id),
            "status": instance.status,
            "amount": str(instance.amount),
        }
    if isinstance(instance, Company):
        return {"name": instance.name, "industry": instance.industry}
    return {}


@receiver(post_save, sender=Deal)
def log_deal_save(sender, instance, created, **kwargs):
    AuditLog.objects.create(
        organization=instance.organization,
        action=AuditLog.Action.CREATE if created else AuditLog.Action.UPDATE,
        entity_type="deal",
        entity_id=str(instance.id),
        changes=_diff(instance),
    )


@receiver(post_save, sender=Company)
def log_company_save(sender, instance, created, **kwargs):
    AuditLog.objects.create(
        organization=instance.organization,
        action=AuditLog.Action.CREATE if created else AuditLog.Action.UPDATE,
        entity_type="company",
        entity_id=str(instance.id),
        changes=_diff(instance),
    )
