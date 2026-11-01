from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.common.models import OrganizationScopedModel


class Company(OrganizationScopedModel):
    name = models.CharField(max_length=150)
    industry = models.CharField(max_length=80, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=80, blank=True)
    country = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="owned_companies",
    )

    class Meta:
        db_table = "crm_company"
        verbose_name_plural = "companies"
        indexes = [
            models.Index(fields=["organization", "name"]),
            models.Index(fields=["organization", "industry"]),
        ]

    def __str__(self):
        return self.name


class Contact(OrganizationScopedModel):
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="contacts",
    )
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    position = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    owner = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="owned_contacts",
    )

    class Meta:
        db_table = "crm_contact"
        indexes = [
            models.Index(fields=["organization", "email"]),
            models.Index(fields=["organization", "phone"]),
            models.Index(fields=["company"]),
        ]

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Pipeline(OrganizationScopedModel):
    name = models.CharField(max_length=120)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "crm_pipeline"
        indexes = [
            models.Index(fields=["organization", "is_default"]),
        ]

    def __str__(self):
        return self.name


class Stage(OrganizationScopedModel):
    pipeline = models.ForeignKey(
        Pipeline, on_delete=models.CASCADE, related_name="stages"
    )
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0, db_index=True)
    color = models.CharField(max_length=7, default="#6366F1")
    is_won = models.BooleanField(default=False)
    is_lost = models.BooleanField(default=False)

    class Meta:
        db_table = "crm_stage"
        ordering = ("order",)
        indexes = [
            models.Index(fields=["pipeline", "order"]),
        ]

    def __str__(self):
        return f"{self.pipeline.name} / {self.name}"


class Lead(OrganizationScopedModel):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        QUALIFIED = "qualified", "Qualified"
        UNQUALIFIED = "unqualified", "Unqualified"

    class Source(models.TextChoices):
        WEB = "web", "Web"
        REFERRAL = "referral", "Referral"
        SOCIAL = "social", "Social"
        EVENT = "event", "Event"
        COLD_CALL = "cold_call", "Cold Call"
        OTHER = "other", "Other"

    title = models.CharField(max_length=200)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="leads",
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="leads",
    )
    source = models.CharField(
        max_length=20, choices=Source.choices, default=Source.OTHER)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW)
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="owned_leads",
    )

    class Meta:
        db_table = "crm_lead"
        indexes = [
            models.Index(fields=["organization", "status", "owner"]),
            models.Index(fields=["organization", "source"]),
        ]

    def __str__(self):
        return self.title


class Deal(OrganizationScopedModel):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        WON = "won", "Won"
        LOST = "lost", "Lost"

    title = models.CharField(max_length=200)
    lead = models.ForeignKey(
        Lead, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="deals",
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="deals")
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="deals",
    )
    pipeline = models.ForeignKey(
        Pipeline, on_delete=models.CASCADE, related_name="deals")
    stage = models.ForeignKey(
        Stage, on_delete=models.CASCADE, related_name="deals")
    amount = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0"))
    currency = models.CharField(max_length=3, default="IRR")
    expected_close_date = models.DateField(null=True, blank=True)
    probability = models.PositiveSmallIntegerField(
        default=50, validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.OPEN)
    order = models.IntegerField(default=0, db_index=True)
    owner = models.ForeignKey(
        "apps.accounts.User" if False else "accounts.User",
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="owned_deals",
    )

    class Meta:
        db_table = "crm_deal"
        ordering = ("order", "-created_at")
        indexes = [
            models.Index(fields=["organization", "pipeline", "stage"]),
            models.Index(fields=["organization", "owner", "status"]),
            models.Index(fields=["organization", "expected_close_date"]),
        ]

    def __str__(self):
        return self.title
