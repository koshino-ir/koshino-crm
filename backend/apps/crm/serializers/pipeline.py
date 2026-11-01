from rest_framework import serializers

from apps.crm.models import Pipeline, Stage


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ["id", "name", "order", "color", "is_won", "is_lost"]
        read_only_fields = ["id"]


class PipelineSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True, read_only=True)

    class Meta:
        model = Pipeline
        fields = ["id", "name", "is_default", "stages", "created_at"]
        read_only_fields = ["id", "created_at"]


class StageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ["name", "order", "color", "is_won", "is_lost"]
