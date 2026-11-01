import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from apps.common.models import BaseModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user with email as the primary identifier."""

    class Language(models.TextChoices):
        FA = "fa", "Persian"
        EN = "en", "English"
        AR = "ar", "Arabic"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    language = models.CharField(
        max_length=2, choices=Language.choices, default=Language.FA)
    google_id = models.CharField(
        max_length=64, unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "accounts_user"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["google_id"]),
        ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)


class Organization(BaseModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=80, unique=True)
    logo = models.ImageField(upload_to="org_logos/", null=True, blank=True)
    timezone = models.CharField(max_length=64, default="Asia/Tehran")
    default_currency = models.CharField(max_length=3, default="IRR")
    default_language = models.CharField(
        max_length=2, choices=User.Language.choices, default="fa")

    members = models.ManyToManyField(
        User, through="Membership", related_name="organizations"
    )

    class Meta:
        db_table = "accounts_organization"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "org"
            slug = base
            counter = 1
            while Organization.all_objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)


class Membership(BaseModel):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(
        max_length=16, choices=Role.choices, default=Role.MEMBER)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "accounts_membership"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "user"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_active_membership",
            ),
        ]
        indexes = [
            models.Index(fields=["organization", "role"]),
            models.Index(fields=["user", "is_active"]),
        ]

    def __str__(self):
        return f"{self.user.email} @ {self.organization.slug} ({self.role})"


class Invitation(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="invitations"
    )
    email = models.EmailField()
    role = models.CharField(
        max_length=16, choices=Membership.Role.choices, default=Membership.Role.MEMBER
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()
    invited_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sent_invitations"
    )
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "accounts_invitation"
        indexes = [
            models.Index(fields=["organization", "email"]),
            models.Index(fields=["token"]),
        ]

    def __str__(self):
        return f"{self.email} → {self.organization.slug}"

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    @property
    def is_usable(self):
        return not self.is_expired and self.accepted_at is None and self.deleted_at is None
