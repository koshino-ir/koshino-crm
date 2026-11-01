from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.mixins import OrgScopedViewMixin
from apps.common.responses import ok
from apps.crm.models import Company, Contact, Deal, Lead


class GlobalSearchView(OrgScopedViewMixin, APIView):
    """
    Quick search across all major entities. Returns top N per category.
    """

    permission_classes = [IsAuthenticated]
    MAX_PER_CATEGORY = 5

    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        if not q or len(q) < 2:
            return ok(data={"query": q, "results": []})

        org = request.organization
        results = []

        for obj in (
            Company.objects.filter(organization=org).filter(
                Q(name__icontains=q) | Q(
                    email__icontains=q) | Q(phone__icontains=q)
            )[: self.MAX_PER_CATEGORY]
        ):
            results.append({
                "type": "company", "id": str(obj.id),
                "title": obj.name, "subtitle": obj.email or obj.phone,
            })

        for obj in (
            Contact.objects.filter(organization=org).filter(
                Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(email__icontains=q)
            )[: self.MAX_PER_CATEGORY]
        ):
            results.append({
                "type": "contact", "id": str(obj.id),
                "title": obj.full_name, "subtitle": obj.email,
            })

        for obj in (
            Deal.objects.filter(organization=org).filter(
                Q(title__icontains=q)
            ).select_related("stage")[: self.MAX_PER_CATEGORY]
        ):
            results.append({
                "type": "deal", "id": str(obj.id),
                "title": obj.title, "subtitle": obj.stage.name,
            })

        for obj in (
            Lead.objects.filter(organization=org).filter(
                Q(title__icontains=q)
            )[: self.MAX_PER_CATEGORY]
        ):
            results.append({
                "type": "lead", "id": str(obj.id),
                "title": obj.title, "subtitle": obj.status,
            })

        return ok(data={"query": q, "results": results})
