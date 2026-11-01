from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.accounts.models import Membership


class IsOrganizationMember(BasePermission):
    """User must be an active member of the target organization."""

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        organization = getattr(obj, "organization", obj)
        return Membership.objects.filter(
            user=request.user,
            organization=organization,
            is_active=True,
        ).exists()


class IsOrganizationAdmin(BasePermission):
    """User must be owner or admin of the target organization."""

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        organization = getattr(obj, "organization", obj)
        return Membership.objects.filter(
            user=request.user,
            organization=organization,
            role__in=[Membership.Role.OWNER, Membership.Role.ADMIN],
            is_active=True,
        ).exists()


class IsOrganizationOwner(BasePermission):
    """User must be the owner of the target organization."""

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        organization = getattr(obj, "organization", obj)
        return Membership.objects.filter(
            user=request.user,
            organization=organization,
            role=Membership.Role.OWNER,
            is_active=True,
        ).exists()
