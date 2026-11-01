from rest_framework import serializers

from apps.crm.models import Contact

from .brief import CompanyBriefSerializer, UserBriefSerializer


class ContactSerializer(serializers.ModelSerializer):
    owner = UserBriefSerializer(read_only=True)
    company = CompanyBriefSerializer(read_only=True)
    company_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Contact
        fields = [
            "id", "first_name", "last_name", "full_name", "email", "phone",
            "position", "is_primary", "company", "company_id", "owner",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "owner",
                            "full_name", "created_at", "updated_at"]

    def validate_company_id(self, value):
        if value is None:
            return None
        request = self.context["request"]
        qs = Company.objects.filter(
            organization=request.organization, id=value)
        if not qs.exists():
            raise serializers.ValidationError(
                "Company not found in this organization.")
        return qs.first()

    def create(self, validated_data):
        company = validated_data.pop("company_id", None)
        return super().create({**validated_data, "company": company})

    def update(self, instance, validated_data):
        if "company_id" in validated_data:
            instance.company = validated_data.pop("company_id")
        return super().update(instance, validated_data)


from apps.crm.models import Company  # noqa: E402
