from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.mixins import OrgScopedViewMixin
from apps.common.responses import ok
from apps.common.views import EnvelopeModelViewMixin
from apps.activities.models import Activity, Task
from apps.activities.selectors import list_activities, list_tasks
from apps.activities.serializers import ActivitySerializer, TaskSerializer


class ActivityListCreateView(OrgScopedViewMixin, EnvelopeModelViewMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return list_activities(
            organization=self.request.organization, params=self.request.query_params
        )

    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.organization, created_by=self.request.user
        )


class ActivityDetailView(OrgScopedViewMixin, EnvelopeModelViewMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivitySerializer
    lookup_url_kwarg = "activity_id"

    def get_queryset(self):
        return Activity.objects.filter(organization=self.request.organization)


class TaskListCreateView(OrgScopedViewMixin, EnvelopeModelViewMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return list_tasks(
            organization=self.request.organization, params=self.request.query_params
        )

    def perform_create(self, serializer):
        serializer.save(organization=self.request.organization)


class TaskDetailView(OrgScopedViewMixin, EnvelopeModelViewMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    lookup_url_kwarg = "task_id"

    def get_queryset(self):
        return Task.objects.filter(organization=self.request.organization)


class TaskCompleteView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        task = get_object_or_404(
            Task, id=task_id, organization=request.organization
        )
        if task.status == Task.Status.DONE:
            return ok(data=TaskSerializer(task).data, message="Task already completed.")
        task.status = Task.Status.DONE
        task.completed_at = timezone.now()
        task.save(update_fields=["status", "completed_at", "updated_at"])
        return ok(data=TaskSerializer(task).data, message="Task completed.")


class TaskReopenView(OrgScopedViewMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        task = get_object_or_404(
            Task, id=task_id, organization=request.organization
        )
        task.status = Task.Status.TODO
        task.completed_at = None
        task.save(update_fields=["status", "completed_at", "updated_at"])
        return ok(data=TaskSerializer(task).data, message="Task reopened.")
