from django.utils import timezone
from rest_framework import serializers

from apps.crm.models import Company, Contact, Deal, Lead

from .models import Activity, Task


class UserBriefSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)


class ActivitySerializer(serializers.ModelSerializer):
    created_by = UserBriefSerializer(read_only=True)
    deal_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)
    lead_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)
    contact_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)
    company_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Activity
        fields = [
            "id", "type", "subject", "description", "occurred_at",
            "deal_id", "lead_id", "contact_id", "company_id",
            "created_by", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def _resolve(self, model, value):
        if value is None:
            return None
        org = self.context["request"].organization
        obj = model.objects.filter(organization=org, id=value).first()
        if not obj:
            raise serializers.ValidationError(
                f"{model.__name__} not found in this organization."
            )
        return obj

    def validate_deal_id(self, v):
        return self._resolve(Deal, v)

    def validate_lead_id(self, v):
        return self._resolve(Lead, v)

    def validate_contact_id(self, v):
        return self._resolve(Contact, v)

    def validate_company_id(self, v):
        return self._resolve(Company, v)

    def validate(self, attrs):
        targets = [
            attrs.get("deal_id") or getattr(self.instance, "deal", None),
            attrs.get("lead_id") or getattr(self.instance, "lead", None),
            attrs.get("contact_id") or getattr(self.instance, "contact", None),
            attrs.get("company_id") or getattr(self.instance, "company", None),
        ]
        if sum(1 for t in targets if t) != 1:
            raise serializers.ValidationError(
                "Exactly one of deal_id, lead_id, contact_id, company_id is required."
            )
        return attrs

    def create(self, validated_data):
        return super().create({
            "deal": validated_data.pop("deal_id", None),
            "lead": validated_data.pop("lead_id", None),
            "contact": validated_data.pop("contact_id", None),
            "company": validated_data.pop("company_id", None),
            **validated_data,
        })

    def update(self, instance, validated_data):
        for key, field in (
            ("deal_id", "deal"),
            ("lead_id", "lead"),
            ("contact_id", "contact"),
            ("company_id", "company"),
        ):
            if key in validated_data:
                setattr(instance, field, validated_data.pop(key))
        return super().update(instance, validated_data)


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserBriefSerializer(read_only=True)
    assigned_to_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)
    deal_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)
    lead_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            "id", "title", "description", "due_date", "priority", "status",
            "completed_at", "assigned_to", "assigned_to_id", "deal_id", "lead_id",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "completed_at", "created_at", "updated_at"]

    def _resolve_user(self, value):
        if value is None:
            return None
        from apps.accounts.models import Membership
        org = self.context["request"].organization
        if not Membership.objects.filter(
            organization=org, user_id=value, is_active=True
        ).exists():
            raise serializers.ValidationError(
                "User is not a member of this organization.")
        from apps.accounts.models import User
        return User.objects.get(id=value)

    def _resolve_deal(self, value):
        if value is None:
            return None
        org = self.context["request"].organization
        obj = Deal.objects.filter(organization=org, id=value).first()
        if not obj:
            raise serializers.ValidationError("Deal not found.")
        return obj

    def _resolve_lead(self, value):
        if value is None:
            return None
        org = self.context["request"].organization
        obj = Lead.objects.filter(organization=org, id=value).first()
        if not obj:
            raise serializers.ValidationError("Lead not found.")
        return obj

    def validate_assigned_to_id(self, v):
        return self._resolve_user(v)

    def validate_deal_id(self, v):
        return self._resolve_deal(v)

    def validate_lead_id(self, v):
        return self._resolve_lead(v)

    def create(self, validated_data):
        return super().create({
            "assigned_to": validated_data.pop("assigned_to_id", None),
            "deal": validated_data.pop("deal_id", None),
            "lead": validated_data.pop("lead_id", None),
            **validated_data,
        })

    def update(self, instance, validated_data):
        for key, field in (
            ("assigned_to_id", "assigned_to"),
            ("deal_id", "deal"),
            ("lead_id", "lead"),
        ):
            if key in validated_data:
                setattr(instance, field, validated_data.pop(key))
        return super().update(instance, validated_data)


class TaskCompleteSerializer(serializers.Serializer):
    pass
