from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.mixins import OrgScopedViewMixin
from apps.common.views import EnvelopeModelViewMixin

from .models import Attachment
from .serializers import AttachmentSerializer


class AttachmentListCreateView(OrgScopedViewMixin, EnvelopeModelViewMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttachmentSerializer

    def get_queryset(self):
        qs = Attachment.objects.filter(
            organization=self.request.organization
        ).select_related("uploaded_by")

        for key in ("deal", "company", "project"):
            if value := self.request.query_params.get(key):
                qs = qs.filter(**{f"{key}_id": value})

        return qs


class AttachmentDetailView(OrgScopedViewMixin, EnvelopeModelViewMixin, RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttachmentSerializer
    lookup_url_kwarg = "attachment_id"

    def get_queryset(self):
        return Attachment.objects.filter(organization=self.request.organization)

    def perform_destroy(self, instance):
        # Soft delete keeps the file around; hard delete removes it too.
        instance.delete()


class AttachmentDownloadView(OrgScopedViewMixin, APIView):
    """
    Secure file serving — never expose MEDIA_URL directly for attachments,
    because that would bypass organization-level access checks.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, attachment_id):
        attachment = get_object_or_404(
            Attachment, id=attachment_id, organization=request.organization
        )
        response = FileResponse(
            attachment.file.open("rb"),
            as_attachment=True,
            filename=attachment.original_name,
            content_type=attachment.mime_type or "application/octet-stream",
        )
        return response
