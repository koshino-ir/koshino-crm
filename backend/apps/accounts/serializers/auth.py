from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.accounts.models import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, style={
                                     "input_type": "password"})
    first_name = serializers.CharField(
        max_length=80, required=False, allow_blank=True)
    last_name = serializers.CharField(
        max_length=80, required=False, allow_blank=True)
    organization_name = serializers.CharField(max_length=120)

    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=attrs["email"].lower(),
            password=attrs["password"],
        )
        if not user:
            raise serializers.ValidationError(
                {"detail": "Invalid credentials."})
        if not user.is_active:
            raise serializers.ValidationError(
                {"detail": "Account is disabled."})
        attrs["user"] = user
        return attrs


class MeSerializer(serializers.ModelSerializer):
    organizations = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "avatar",
            "language", "organizations",
        ]
        read_only_fields = ["id", "email", "organizations"]

    def get_organizations(self, user):
        memberships = user.memberships.filter(
            is_active=True).select_related("organization")
        return [
            {
                "id": str(m.organization.id),
                "name": m.organization.name,
                "slug": m.organization.slug,
                "role": m.role,
            }
            for m in memberships
        ]


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        validate_password(value, self.context["request"].user)
        return value
