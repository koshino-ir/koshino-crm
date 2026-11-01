from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.projects.models import Invoice


def _generate_number(organization) -> str:
    year = timezone.now().year
    count = Invoice.all_objects.filter(organization=organization).count() + 1
    return f"INV-{year}-{count:04d}"


@transaction.atomic
def create_invoice(*, organization, serializer, project):
    """
    Create an invoice with an auto-generated number if missing.
    Retries with a new number on the (rare) unique-constraint collision.
    """
    data = serializer.validated_data
    number = data.pop("number", "") or _generate_number(organization)

    for attempt in range(3):
        try:
            return serializer.save(
                organization=organization, project=project, number=number
            )
        except IntegrityError:
            if attempt == 2:
                raise ValueError("Could not generate a unique invoice number.")
            number = _generate_number(organization)

    raise ValueError("Could not generate a unique invoice number.")


@transaction.atomic
def mark_paid(*, invoice):
    if invoice.status == Invoice.Status.PAID:
        return invoice
    invoice.status = Invoice.Status.PAID
    invoice.paid_at = timezone.now()
    invoice.save(update_fields=["status", "paid_at", "updated_at"])
    return invoice
