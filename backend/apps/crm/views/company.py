from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.common.mixins import OrgScopedViewMixin
from apps.common.views import EnvelopeModelViewMixin
from apps.crm.models import Company
from apps.crm.selectors import list_companies
from apps.crm.serializers.company import CompanySerializer


class CompanyListCreateView(OrgScopedViewMixin, EnvelopeModelViewMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer

    def get_queryset(self):
        return list_companies(
            organization=self.request.organization, params=self.request.query_params
        )

    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.organization, owner=self.request.user
        )


class CompanyDetailView(OrgScopedViewMixin, EnvelopeModelViewMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer
    lookup_url_kwarg = "company_id"

    def get_queryset(self):
        return Company.objects.filter(organization=self.request.organization)
