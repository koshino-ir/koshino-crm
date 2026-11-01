from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.mixins import OrgScopedViewMixin
from apps.common.responses import ok
from apps.common.views import EnvelopeModelViewMixin
from apps.projects.models import Invoice, Project
from apps.projects.selectors import list_invoices
from apps.projects.serializers import InvoiceSerializer
from apps.projects.services.invoice_service import create_invoice, mark_paid


class InvoiceListCreateView(OrgScopedViewMixin, EnvelopeModelViewMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return list_invoices(
            organization=self.request.organization, params=self.request.query_params
        )

    def perform_create(self, serializer):
        data = serializer.validated_data
        project_id = data.pop("project_id", None)
        if not project_id:
            raise ValidationError({"project_id": "This field is required."})
        project = get_object_or_404(
            Project, id=project_id, organization=self.request.organization
        )
        try:
            create_invoice(
                organization=self.request.organization,
                serializer=serializer,
                project=project,
            )
        except ValueError as exc:
            raise ValidationError({"detail": str(exc)})


class InvoiceDetailView(OrgScopedViewMixin, EnvelopeModelViewMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer
    lookup_url_kwarg = "invoice_id"

    def get_queryset(self):
        return Invoice.objects.filter(organization=self.request.organization).select_related("project")


class InvoiceMarkPaidView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, invoice_id):
        invoice = get_object_or_404(
            Invoice, id=invoice_id, organization=request.organization
        )
        invoice = mark_paid(invoice=invoice)
        return ok(data=InvoiceSerializer(invoice).data, message="Invoice marked as paid.")
