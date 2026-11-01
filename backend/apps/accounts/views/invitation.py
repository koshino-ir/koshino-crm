from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.accounts.models import Invitation, Organization
from apps.accounts.selectors import get_user_membership
from apps.accounts.serializers.organization import (
    InvitationAcceptSerializer, InvitationCreateSerializer,
)
from apps.accounts.services.invite_service import accept_invitation, create_invitation
from apps.common.permissions import IsOrganizationAdmin
from apps.common.responses import APIResponse, ok, created


class InvitationCreateView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationAdmin]
    throttle_scope = "invitation"

    def post(self, request, org_id):
        org = get_object_or_404(Organization, id=org_id)
        self.check_object_permissions(request, org)
        serializer = InvitationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            invitation = create_invitation(
                organization=org,
                email=serializer.validated_data["email"],
                role=serializer.validated_data["role"],
                invited_by=request.user,
            )
        except ValueError as exc:
            return APIResponse(success=False, message=str(exc), status=400)
        return created(
            data={"id": str(invitation.id), "email": invitation.email,
                  "token": str(invitation.token)},
            message="Invitation created.",
        )


class InvitationAcceptView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InvitationAcceptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invitation = Invitation.objects.filter(
            token=serializer.validated_data["token"]).first()
        if not invitation or not invitation.is_usable:
            return APIResponse(success=False, message="Invalid or expired invitation.", status=400)

        if not request.user.is_authenticated:
            return APIResponse(
                success=False,
                message="Please sign in or register with the invited email first.",
                status=401,
            )
        try:
            accept_invitation(token=invitation.token, user=request.user)
        except ValueError as exc:
            return APIResponse(success=False, message=str(exc), status=400)
        return ok(message="Invitation accepted.")
