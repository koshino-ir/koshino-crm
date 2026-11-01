from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Invitation, Membership


@transaction.atomic
def create_invitation(*, organization, email, role, invited_by):
    email = email.lower()
    if Membership.objects.filter(
        organization=organization, user__email=email, is_active=True
    ).exists():
        raise ValueError("User is already a member.")

    # Expire any pending invitation for this email
    Invitation.objects.filter(
        organization=organization, email=email, accepted_at__isnull=True
    ).update(deleted_at=timezone.now())

    return Invitation.objects.create(
        organization=organization,
        email=email,
        role=role,
        invited_by=invited_by,
        expires_at=timezone.now() + timedelta(days=7),
    )


@transaction.atomic
def accept_invitation(*, token, user):
    invitation = Invitation.objects.filter(
        token=token, accepted_at__isnull=True).first()
    if not invitation:
        raise ValueError("Invitation not found.")
    if invitation.is_expired:
        raise ValueError("Invitation has expired.")
    if invitation.email != user.email.lower():
        raise ValueError("This invitation belongs to a different email.")

    membership, _ = Membership.objects.get_or_create(
        organization=invitation.organization,
        user=user,
        defaults={"role": invitation.role, "is_active": True},
    )
    if not membership.is_active:
        membership.is_active = True
        membership.save(update_fields=["is_active", "updated_at"])

    invitation.accepted_at = timezone.now()
    invitation.save(update_fields=["accepted_at", "updated_at"])
    return membership
