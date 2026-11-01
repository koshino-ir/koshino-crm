from rest_framework import serializers

from apps.crm.models import Company, Contact, Lead

from .brief import CompanyBriefSerializer, ContactBriefSerializer, UserBriefSerializer


class LeadSerializer(serializers.ModelSerializer):
    owner = UserBriefSerializer(read_only=True)
    company = CompanyBriefSerializer(read_only=True)
    contact = ContactBriefSerializer(read_only=True)
    company_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)
    contact_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Lead
        fields = [
            "id", "title", "source", "status", "notes",
            "company", "company_id", "contact", "contact_id",
            "owner", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    def _resolve_fk(self, model, value):
        if value is None:
            return None
        org = self.context["request"].organization
        obj = model.objects.filter(organization=org, id=value).first()
        if not obj:
            raise serializers.ValidationError(
                f"{model.__name__} not found in this organization.")
        return obj

    def validate_company_id(self, value):
        return self._resolve_fk(Company, value)

    def validate_contact_id(self, value):
        return self._resolve_fk(Contact, value)

    def create(self, validated_data):
        company = validated_data.pop("company_id", None)
        contact = validated_data.pop("contact_id", None)
        return super().create({**validated_data, "company": company, "contact": contact})

    def update(self, instance, validated_data):
        if "company_id" in validated_data:
            instance.company = validated_data.pop("company_id")
        if "contact_id" in validated_data:
            instance.contact = validated_data.pop("contact_id")
        return super().update(instance, validated_data)


class LeadConvertSerializer(serializers.Serializer):
    pipeline_id = serializers.UUIDField()
    stage_id = serializers.UUIDField(required=False, allow_null=True)
