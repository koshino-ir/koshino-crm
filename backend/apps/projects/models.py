from decimal import Decimal, InvalidOperation

from django.core.validators import MinValueValidator
from django.db import models

from apps.common.models import OrganizationScopedModel


class Project(OrganizationScopedModel):
    class Status(models.TextChoices):
        PLANNING = "planning", "Planning"
        ACTIVE = "active", "Active"
        ON_HOLD = "on_hold", "On hold"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.PLANNING
    )
    deal = models.ForeignKey(
        "crm.Deal", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="projects",
    )
    client_company = models.ForeignKey(
        "crm.Company", on_delete=models.CASCADE, related_name="projects"
    )
    owner = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="owned_projects",
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )

    class Meta:
        db_table = "projects_project"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["organization", "client_company"]),
            models.Index(fields=["deal"]),
        ]

    def __str__(self):
        return self.name


class Invoice(OrganizationScopedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SENT = "sent", "Sent"
        PAID = "paid", "Paid"
        OVERDUE = "overdue", "Overdue"
        CANCELLED = "cancelled", "Cancelled"

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="invoices"
    )
    number = models.CharField(max_length=40)
    amount = models.DecimalField(
        max_digits=14, decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )
    tax = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    total = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0"), editable=False,
    )
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.DRAFT
    )
    issue_date = models.DateField()
    due_date = models.DateField()
    paid_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "projects_invoice"
        ordering = ("-issue_date",)
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "number"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_invoice_number_per_org",
            ),
        ]
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["organization", "due_date"]),
            models.Index(fields=["project"]),
        ]

    def __str__(self):
        return f"{self.number} ({self.total})"

    def save(self, *args, **kwargs):
        def _to_decimal(value) -> Decimal:
            if isinstance(value, Decimal):
                return value
            if value is None or value == "":
                return Decimal("0")
            try:
                return Decimal(str(value))
            except (InvalidOperation, ValueError):
                return Decimal("0")

        self.total = _to_decimal(self.amount) + _to_decimal(self.tax)
        super().save(*args, **kwargs)
