from rest_framework.exceptions import PermissionDenied

from apps.accounts.models import Membership


class OrgScopedViewMixin:
    """
    Resolves the current organization for the request.

    Priority:
    1. Header `X-Organization-Id` (must be an org the user belongs to)
    2. First active membership (fallback)

    Sets `request.organization` and `request.membership`.
    All views that need org-scoping must inherit from this mixin.
    """

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if not request.user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        org_id = request.headers.get("X-Organization-Id")
        qs = (
            Membership.objects
            .filter(user=request.user, is_active=True)
            .select_related("organization")
        )
        membership = None
        if org_id:
            membership = qs.filter(organization_id=org_id).first()
        if not membership:
            membership = qs.order_by("joined_at").first()

        if not membership:
            raise PermissionDenied("You are not a member of any organization.")

        request.membership = membership
        request.organization = membership.organization
