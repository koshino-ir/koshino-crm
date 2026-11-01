from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.accounts.models import Membership, Organization
from apps.accounts.serializers.organization import (
    MembershipSerializer, OrganizationSerializer,
)
from apps.accounts.selectors import get_user_membership
from apps.common.permissions import IsOrganizationAdmin, IsOrganizationOwner
from apps.common.responses import APIResponse, ok, created, no_content


class OrganizationListCreateView(APIView):
    def get(self, request):
        orgs = (
            Organization.objects.filter(
                memberships__user=request.user, memberships__is_active=True)
            .distinct()
            .order_by("name")
        )
        return ok(data=OrganizationSerializer(orgs, many=True, context={"request": request}).data)

    def post(self, request):
        serializer = OrganizationSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        with __import__("django.db").db.transaction.atomic():
            org = serializer.save()
            Membership.objects.create(
                organization=org, user=request.user, role=Membership.Role.OWNER,
            )
        return created(
            data=OrganizationSerializer(
                org, context={"request": request}).data,
            message="Organization created.",
        )


class OrganizationDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]

    def get_object(self, request, org_id):
        org = get_object_or_404(Organization, id=org_id)
        self.check_object_permissions(request, org)
        return org

    def get(self, request, org_id):
        org = self.get_object(request, org_id)
        return ok(data=OrganizationSerializer(org, context={"request": request}).data)

    def patch(self, request, org_id):
        org = self.get_object(request, org_id)
        serializer = OrganizationSerializer(
            org, data=request.data, partial=True, context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ok(data=serializer.data, message="Organization updated.")

    def delete(self, request, org_id):
        org = get_object_or_404(Organization, id=org_id)
        self.check_object_permissions(request, org)
        if not IsOrganizationOwner().has_object_permission(request, self, org):
            return APIResponse(success=False, message="Only the owner can delete.", status=403)
        org.delete()
        return no_content("Organization deleted.")


class OrganizationMemberListView(APIView):
    def get(self, request, org_id):
        org = get_object_or_404(Organization, id=org_id)
        if not get_user_membership(request.user, org.id):
            return APIResponse(success=False, message="Access denied.", status=403)
        memberships = org.memberships.filter(
            is_active=True).select_related("user")
        return ok(data=MembershipSerializer(memberships, many=True).data)


class OrganizationMemberDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]

    def patch(self, request, org_id, member_id):
        org = get_object_or_404(Organization, id=org_id)
        self.check_object_permissions(request, org)
        membership = get_object_or_404(
            Membership, id=member_id, organization=org)
        if membership.role == Membership.Role.OWNER:
            return APIResponse(success=False, message="Cannot modify owner.", status=400)
        serializer = MembershipSerializer(
            membership, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ok(data=serializer.data, message="Member updated.")

    def delete(self, request, org_id, member_id):
        org = get_object_or_404(Organization, id=org_id)
        self.check_object_permissions(request, org)
        membership = get_object_or_404(
            Membership, id=member_id, organization=org)
        if membership.role == Membership.Role.OWNER:
            return APIResponse(success=False, message="Cannot remove owner.", status=400)
        membership.delete()
        return no_content("Member removed.")
