from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.mixins import OrgScopedViewMixin
from apps.common.responses import ok
from apps.common.views import EnvelopeModelViewMixin
from apps.crm.models import Deal, Stage
from apps.crm.selectors import kanban_board, list_deals
from apps.crm.serializers.deal import DealMoveSerializer, DealSerializer
from apps.crm.services.deal_service import create_deal, move_deal


class DealListCreateView(OrgScopedViewMixin, EnvelopeModelViewMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DealSerializer

    def get_queryset(self):
        return list_deals(
            organization=self.request.organization, params=self.request.query_params
        )

    def perform_create(self, serializer):
        create_deal(organization=self.request.organization,
                    serializer=serializer)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        return ctx


class DealDetailView(OrgScopedViewMixin, EnvelopeModelViewMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DealSerializer
    lookup_url_kwarg = "deal_id"

    def get_queryset(self):
        return Deal.objects.filter(organization=self.request.organization)


class DealKanbanView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pipeline_id = request.query_params.get("pipeline")
        if not pipeline_id:
            raise ValidationError(
                {"pipeline": "This query parameter is required."})
        board = kanban_board(
            organization=request.organization, pipeline_id=pipeline_id
        )
        if board is None:
            from rest_framework.exceptions import NotFound
            raise NotFound("Pipeline not found.")
        return ok(data={
            "pipeline": {
                "id": str(board["pipeline"].id),
                "name": board["pipeline"].name,
            },
            "stages": [
                {
                    **{k: v for k, v in s.items() if k != "deals"},
                    "deals": DealSerializer(s["deals"], many=True).data,
                }
                for s in board["stages"]
            ],
        })


class DealMoveView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, deal_id):
        deal = get_object_or_404(
            Deal, id=deal_id, organization=request.organization
        )
        serializer = DealMoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        stage = get_object_or_404(
            Stage,
            id=serializer.validated_data["stage_id"],
            organization=request.organization,
        )
        try:
            deal = move_deal(
                deal=deal,
                stage=stage,
                order=serializer.validated_data.get("order"),
            )
        except ValueError as exc:
            raise ValidationError({"detail": str(exc)})

        return ok(data=DealSerializer(deal).data, message="Deal moved.")
