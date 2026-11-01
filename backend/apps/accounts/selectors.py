from .models import Membership, Organization


def get_user_organizations(user):
    """Return active orgs the user belongs to, with their role."""
    return (
        Membership.objects.filter(user=user, is_active=True)
        .select_related("organization")
        .order_by("organization__name")
    )


def get_user_membership(user, organization_id):
    if not user.is_authenticated:
        return None
    return (
        Membership.objects.filter(
            user=user, organization_id=organization_id, is_active=True
        )
        .select_related("organization")
        .first()
    )
