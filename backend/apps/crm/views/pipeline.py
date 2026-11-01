from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.mixins import OrgScopedViewMixin
from apps.common.responses import APIResponse, ok, created
from apps.crm.models import Pipeline, Stage
from apps.crm.selectors import get_pipeline_with_stages, list_pipelines
from apps.crm.services.pipeline_service import ensure_default_pipeline
from apps.crm.serializers.pipeline import (
    PipelineSerializer, StageSerializer, StageWriteSerializer,
)


class PipelineListCreateView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = list_pipelines(organization=request.organization,
                            params=request.query_params)
        return ok(data=PipelineSerializer(qs, many=True).data)

    def post(self, request):
        serializer = PipelineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            pipeline = serializer.save(organization=request.organization)
        return created(
            data=PipelineSerializer(pipeline).data, message="Pipeline created."
        )


class PipelineDetailView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def _get(self, request, pipeline_id):
        pipeline = get_pipeline_with_stages(
            organization=request.organization, pipeline_id=pipeline_id
        )
        if not pipeline:
            from rest_framework.exceptions import NotFound
            raise NotFound("Pipeline not found.")
        return pipeline

    def get(self, request, pipeline_id):
        pipeline = self._get(request, pipeline_id)
        return ok(data=PipelineSerializer(pipeline).data)

    def patch(self, request, pipeline_id):
        pipeline = self._get(request, pipeline_id)
        serializer = PipelineSerializer(
            pipeline, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ok(data=serializer.data, message="Pipeline updated.")

    def delete(self, request, pipeline_id):
        pipeline = self._get(request, pipeline_id)
        pipeline.delete()
        return APIResponse(message="Pipeline deleted.", status=204)


class StageListCreateView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def _pipeline(self, request, pipeline_id):
        pipeline = get_pipeline_with_stages(
            organization=request.organization, pipeline_id=pipeline_id
        )
        if not pipeline:
            from rest_framework.exceptions import NotFound
            raise NotFound("Pipeline not found.")
        return pipeline

    def get(self, request, pipeline_id):
        pipeline = self._pipeline(request, pipeline_id)
        return ok(data=StageSerializer(pipeline.stages.all(), many=True).data)

    def post(self, request, pipeline_id):
        pipeline = self._pipeline(request, pipeline_id)
        serializer = StageWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stage = serializer.save(
            organization=request.organization, pipeline=pipeline)
        return created(data=StageSerializer(stage).data, message="Stage created.")


class StageDetailView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def _get(self, request, stage_id):
        stage = get_object_or_404(
            Stage, id=stage_id, organization=request.organization
        )
        return stage

    def patch(self, request, stage_id):
        stage = self._get(request, stage_id)
        serializer = StageWriteSerializer(
            stage, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ok(data=StageSerializer(stage).data, message="Stage updated.")

    def delete(self, request, stage_id):
        stage = self._get(request, stage_id)
        stage.delete()
        return APIResponse(message="Stage deleted.", status=204)


class PipelineEnsureDefaultView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pipeline = ensure_default_pipeline(organization=request.organization)
        return ok(
            data=PipelineSerializer(pipeline).data,
            message="Default pipeline ready.",
        )
