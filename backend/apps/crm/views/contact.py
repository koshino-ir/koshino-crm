from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.common.mixins import OrgScopedViewMixin
from apps.common.views import EnvelopeModelViewMixin
from apps.crm.models import Contact
from apps.crm.selectors import list_contacts
from apps.crm.serializers.contact import ContactSerializer


class ContactListCreateView(OrgScopedViewMixin, EnvelopeModelViewMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def get_queryset(self):
        return list_contacts(
            organization=self.request.organization, params=self.request.query_params
        )

    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.organization, owner=self.request.user
        )


class ContactDetailView(OrgScopedViewMixin, EnvelopeModelViewMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer
    lookup_url_kwarg = "contact_id"

    def get_queryset(self):
        return Contact.objects.filter(organization=self.request.organization)
