from rest_framework import serializers

from apps.crm.models import Company, Deal

from .models import Invoice, Project


class CompanyBriefSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)


class UserBriefSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)


class DealBriefSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(read_only=True)


class ProjectSerializer(serializers.ModelSerializer):
    client_company = CompanyBriefSerializer(read_only=True)
    owner = UserBriefSerializer(read_only=True)
    deal = DealBriefSerializer(read_only=True)
    client_company_id = serializers.UUIDField(write_only=True)
    deal_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)
    invoices_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "name", "description", "status", "start_date", "end_date",
            "budget", "client_company", "client_company_id",
            "deal", "deal_id", "owner", "invoices_count",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "owner",
                            "invoices_count", "created_at", "updated_at"]

    def _resolve_company(self, value):
        org = self.context["request"].organization
        obj = Company.objects.filter(organization=org, id=value).first()
        if not obj:
            raise serializers.ValidationError("Company not found.")
        return obj

    def _resolve_deal(self, value):
        if value is None:
            return None
        org = self.context["request"].organization
        obj = Deal.objects.filter(organization=org, id=value).first()
        if not obj:
            raise serializers.ValidationError("Deal not found.")
        return obj

    def validate_client_company_id(self, v):
        return self._resolve_company(v)

    def validate_deal_id(self, v):
        return self._resolve_deal(v)

    def validate(self, attrs):
        start = attrs.get("start_date") or getattr(
            self.instance, "start_date", None)
        end = attrs.get("end_date") or getattr(self.instance, "end_date", None)
        if start and end and end < start:
            raise serializers.ValidationError(
                {"end_date": "End date must be on or after start date."}
            )
        return attrs

    def get_invoices_count(self, obj):
        return getattr(obj, "invoices_count", obj.invoices.count())

    def create(self, validated_data):
        return super().create({
            "client_company": validated_data.pop("client_company_id"),
            "deal": validated_data.pop("deal_id", None),
            **validated_data,
        })

    def update(self, instance, validated_data):
        if "client_company_id" in validated_data:
            instance.client_company = validated_data.pop("client_company_id")
        if "deal_id" in validated_data:
            instance.deal = validated_data.pop("deal_id")
        return super().update(instance, validated_data)


class InvoiceSerializer(serializers.ModelSerializer):
    number = serializers.CharField(
        max_length=40, required=False, allow_blank=True
    )
    project_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Invoice
        fields = [
            "id", "number", "amount", "tax", "total",
            "status", "issue_date", "due_date", "paid_at", "notes",
            "project_id", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "total", "paid_at", "created_at", "updated_at",
        ]

    def validate(self, attrs):
        issue = attrs.get("issue_date") or getattr(
            self.instance, "issue_date", None)
        due = attrs.get("due_date") or getattr(self.instance, "due_date", None)
        if issue and due and due < issue:
            raise serializers.ValidationError(
                {"due_date": "Due date must be on or after issue date."}
            )
        return attrs
