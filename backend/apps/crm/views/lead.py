from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.mixins import OrgScopedViewMixin
from apps.common.responses import ok
from apps.common.views import EnvelopeModelViewMixin
from apps.crm.models import Lead, Pipeline, Stage
from apps.crm.selectors import list_leads
from apps.crm.serializers.deal import DealSerializer
from apps.crm.serializers.lead import LeadConvertSerializer, LeadSerializer
from apps.crm.services.deal_service import convert_lead_to_deal


class LeadListCreateView(OrgScopedViewMixin, EnvelopeModelViewMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeadSerializer

    def get_queryset(self):
        return list_leads(
            organization=self.request.organization, params=self.request.query_params
        )

    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.organization, owner=self.request.user
        )


class LeadDetailView(OrgScopedViewMixin, EnvelopeModelViewMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeadSerializer
    lookup_url_kwarg = "lead_id"

    def get_queryset(self):
        return Lead.objects.filter(organization=self.request.organization)


class LeadConvertView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lead_id):
        lead = get_object_or_404(
            Lead, id=lead_id, organization=request.organization
        )
        serializer = LeadConvertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pipeline = get_object_or_404(
            Pipeline,
            id=serializer.validated_data["pipeline_id"],
            organization=request.organization,
        )
        stage = None
        if stage_id := serializer.validated_data.get("stage_id"):
            stage = get_object_or_404(
                Stage, id=stage_id, organization=request.organization
            )

        try:
            deal = convert_lead_to_deal(
                lead=lead,
                pipeline=pipeline,
                stage=stage,
                owner=request.user,
            )
        except ValueError as exc:
            raise ValidationError({"detail": str(exc)})

        return ok(data=DealSerializer(deal).data, message="Lead converted to deal.")
