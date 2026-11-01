from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.common.mixins import OrgScopedViewMixin
from apps.common.views import EnvelopeModelViewMixin
from apps.projects.models import Project
from apps.projects.selectors import list_projects
from apps.projects.serializers import ProjectSerializer


class ProjectListCreateView(OrgScopedViewMixin, EnvelopeModelViewMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return list_projects(
            organization=self.request.organization, params=self.request.query_params
        )

    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.organization, owner=self.request.user
        )


class ProjectDetailView(OrgScopedViewMixin, EnvelopeModelViewMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    lookup_url_kwarg = "project_id"

    def get_queryset(self):
        return Project.objects.filter(organization=self.request.organization).select_related(
            "client_company", "owner", "deal"
        )
