from rest_framework import serializers

from apps.crm.models import Company, Deal
from apps.projects.models import Project

from .models import Attachment
from .services.upload_service import validate_upload


class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    download_url = serializers.SerializerMethodField()
    deal_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)
    company_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)
    project_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Attachment
        fields = [
            "id", "file", "original_name", "mime_type", "size", "download_url",
            "deal_id", "company_id", "project_id", "uploaded_by",
            "created_at",
        ]
        read_only_fields = [
            "id", "original_name", "mime_type", "size", "download_url",
            "uploaded_by", "created_at",
        ]

    def _resolve(self, model, value, field):
        if value is None:
            return None
        org = self.context["request"].organization
        obj = model.objects.filter(organization=org, id=value).first()
        if not obj:
            raise serializers.ValidationError(
                {field: f"{model.__name__} not found."})
        return obj

    def validate_deal_id(self, v):
        return self._resolve(Deal, v, "deal_id")

    def validate_company_id(self, v):
        return self._resolve(Company, v, "company_id")

    def validate_project_id(self, v):
        return self._resolve(Project, v, "project_id")

    def validate(self, attrs):
        targets = [
            attrs.get("deal_id"),
            attrs.get("company_id"),
            attrs.get("project_id"),
        ]
        if sum(1 for t in targets if t) != 1:
            raise serializers.ValidationError(
                "Exactly one of deal_id, company_id, project_id is required."
            )

        file_obj = attrs.get("file")
        if file_obj:
            validate_upload(file_obj)
        return attrs

    def get_download_url(self, obj):
        return f"/api/v1/attachments/{obj.id}/download/"

    def create(self, validated_data):
        file_obj = validated_data["file"]
        return Attachment.objects.create(
            organization=self.context["request"].organization,
            uploaded_by=self.context["request"].user,
            original_name=file_obj.name,
            mime_type=file_obj.content_type or "",
            size=file_obj.size,
            file=file_obj,
            deal=validated_data.pop("deal_id", None),
            company=validated_data.pop("company_id", None),
            project=validated_data.pop("project_id", None),
        )
