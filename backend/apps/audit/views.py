from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import PermissionDenied

from apps.accounts.models import Membership
from apps.common.mixins import OrgScopedViewMixin
from apps.common.permissions import IsOrganizationAdmin

from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogListView(OrgScopedViewMixin, ListAPIView):
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        role = self.request.membership.role
        if role not in (Membership.Role.OWNER, Membership.Role.ADMIN):
            raise PermissionDenied(
                "Only owners and admins can view audit logs.")
        qs = AuditLog.objects.filter(organization=self.request.organization)
        if entity_type := self.request.query_params.get("entity_type"):
            qs = qs.filter(entity_type=entity_type)
        if entity_id := self.request.query_params.get("entity_id"):
            qs = qs.filter(entity_id=entity_id)
        return qs

    def get_permissions(self):
        # IsOrganizationAdmin expects an object; adapt for list-only view
        return [IsAuthenticated()]
