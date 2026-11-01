from rest_framework import serializers

from apps.crm.models import Company

from .brief import UserBriefSerializer


class CompanySerializer(serializers.ModelSerializer):
    owner = UserBriefSerializer(read_only=True)
    contacts_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            "id", "name", "industry", "website", "phone", "email",
            "address", "city", "country", "notes", "owner",
            "contacts_count", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "owner",
                            "contacts_count", "created_at", "updated_at"]

    def get_contacts_count(self, obj):
        # Uses prefetched count if available (selector should annotate)
        return getattr(obj, "contacts_count", obj.contacts.count())
