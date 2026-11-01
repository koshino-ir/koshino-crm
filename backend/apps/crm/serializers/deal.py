from rest_framework import serializers

from apps.crm.models import Company, Contact, Deal, Pipeline, Stage

from .brief import CompanyBriefSerializer, ContactBriefSerializer, UserBriefSerializer


class PipelineBriefSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)


class StageBriefSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    color = serializers.CharField(read_only=True)


class DealSerializer(serializers.ModelSerializer):
    owner = UserBriefSerializer(read_only=True)
    company = CompanyBriefSerializer(read_only=True)
    contact = ContactBriefSerializer(read_only=True)
    pipeline = PipelineBriefSerializer(read_only=True)
    stage = StageBriefSerializer(read_only=True)
    company_id = serializers.UUIDField(write_only=True)
    contact_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)
    pipeline_id = serializers.UUIDField(write_only=True)
    stage_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Deal
        fields = [
            "id", "title", "amount", "currency", "expected_close_date",
            "probability", "status", "order",
            "company", "company_id", "contact", "contact_id",
            "pipeline", "pipeline_id", "stage", "stage_id", "owner",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "owner", "order",
                            "status", "created_at", "updated_at"]

    def _resolve(self, model, value):
        org = self.context["request"].organization
        obj = model.objects.filter(organization=org, id=value).first()
        if not obj:
            raise serializers.ValidationError(
                f"{model.__name__} not found in this organization.")
        return obj

    def validate_company_id(self, value):
        return self._resolve(Company, value)

    def validate_contact_id(self, value):
        return None if value is None else self._resolve(Contact, value)

    def validate_pipeline_id(self, value):
        return self._resolve(Pipeline, value)

    def validate_stage_id(self, value):
        return None if value is None else self._resolve(Stage, value)

    def validate(self, attrs):
        # On update we may receive only some fields — pull existing values.
        pipeline = attrs.get("pipeline_id") or getattr(
            self.instance, "pipeline", None)
        stage = attrs.get("stage_id") or getattr(self.instance, "stage", None)
        if pipeline and stage and stage.pipeline_id != pipeline.id:
            raise serializers.ValidationError(
                {"stage_id": "Stage is not part of this pipeline."})
        return attrs

    def create(self, validated_data):
        company = validated_data.pop("company_id")
        contact = validated_data.pop("contact_id", None)
        pipeline = validated_data.pop("pipeline_id")
        stage = validated_data.pop("stage_id", None)
        return super().create({
            **validated_data,
            "company": company,
            "contact": contact,
            "pipeline": pipeline,
            "stage": stage,
        })

    def update(self, instance, validated_data):
        if "company_id" in validated_data:
            instance.company = validated_data.pop("company_id")
        if "contact_id" in validated_data:
            instance.contact = validated_data.pop("contact_id")
        if "pipeline_id" in validated_data:
            instance.pipeline = validated_data.pop("pipeline_id")
        if "stage_id" in validated_data:
            instance.stage = validated_data.pop("stage_id")
        return super().update(instance, validated_data)


class DealMoveSerializer(serializers.Serializer):
    stage_id = serializers.UUIDField()
    order = serializers.IntegerField(
        required=False, allow_null=True, min_value=0)
