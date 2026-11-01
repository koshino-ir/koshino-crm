from rest_framework import serializers

from apps.accounts.models import Invitation, Membership, Organization, User


class OrganizationSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            "id", "name", "slug", "logo", "timezone",
            "default_currency", "default_language", "role",
            "created_at",
        ]
        read_only_fields = ["id", "slug", "created_at"]

    def get_role(self, org):
        user = self.context["request"].user
        m = org.memberships.filter(user=user, is_active=True).first()
        return m.role if m else None


class MembershipSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = ["id", "user", "role", "is_active", "joined_at"]
        read_only_fields = ["id", "user", "joined_at"]

    def get_user(self, m):
        return {
            "id": str(m.user.id),
            "email": m.user.email,
            "first_name": m.user.first_name,
            "last_name": m.user.last_name,
            "avatar": m.user.avatar.url if m.user.avatar else None,
        }


class InvitationCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=Membership.Role.choices, default=Membership.Role.MEMBER)


class InvitationAcceptSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    password = serializers.CharField(
        write_only=True, min_length=8, required=False)
    first_name = serializers.CharField(
        max_length=80, required=False, allow_blank=True)
    last_name = serializers.CharField(
        max_length=80, required=False, allow_blank=True)
