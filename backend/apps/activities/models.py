from django.db import models

from apps.common.models import OrganizationScopedModel


class Activity(OrganizationScopedModel):
    """
    A logged interaction. Polymorphic link via nullable FKs —
    exactly one of (deal, lead, contact, company) should be set.
    """

    class Type(models.TextChoices):
        CALL = "call", "Call"
        EMAIL = "email", "Email"
        MEETING = "meeting", "Meeting"
        NOTE = "note", "Note"

    type = models.CharField(max_length=16, choices=Type.choices)
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    occurred_at = models.DateTimeField(db_index=True)

    deal = models.ForeignKey(
        "crm.Deal", on_delete=models.CASCADE, null=True, blank=True,
        related_name="activities",
    )
    lead = models.ForeignKey(
        "crm.Lead", on_delete=models.CASCADE, null=True, blank=True,
        related_name="activities",
    )
    contact = models.ForeignKey(
        "crm.Contact", on_delete=models.CASCADE, null=True, blank=True,
        related_name="activities",
    )
    company = models.ForeignKey(
        "crm.Company", on_delete=models.CASCADE, null=True, blank=True,
        related_name="activities",
    )

    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True,
        related_name="created_activities",
    )

    class Meta:
        db_table = "activities_activity"
        ordering = ("-occurred_at",)
        indexes = [
            models.Index(fields=["organization", "occurred_at"]),
            models.Index(fields=["organization", "type"]),
            models.Index(fields=["deal"]),
            models.Index(fields=["lead"]),
            models.Index(fields=["company"]),
        ]

    def __str__(self):
        return f"{self.type}: {self.subject}"

    def save(self, *args, **kwargs):
        # Enforce that exactly one of the four relation FKs is set
        targets = [self.deal_id, self.lead_id,
                   self.contact_id, self.company_id]
        if sum(1 for t in targets if t) != 1:
            raise ValueError(
                "Activity must be linked to exactly one of: deal, lead, contact, company."
            )
        super().save(*args, **kwargs)


class Task(OrganizationScopedModel):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    class Status(models.TextChoices):
        TODO = "todo", "To do"
        IN_PROGRESS = "in_progress", "In progress"
        DONE = "done", "Done"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True, db_index=True)
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.TODO)
    completed_at = models.DateTimeField(null=True, blank=True)

    assigned_to = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="assigned_tasks",
    )
    deal = models.ForeignKey(
        "crm.Deal", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="tasks",
    )
    lead = models.ForeignKey(
        "crm.Lead", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="tasks",
    )

    class Meta:
        db_table = "activities_task"
        ordering = ("status", "due_date", "-created_at")
        indexes = [
            models.Index(fields=["organization", "assigned_to", "status"]),
            models.Index(fields=["organization", "status", "due_date"]),
        ]

    def __str__(self):
        return self.title
