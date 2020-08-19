from rest_framework import serializers

from .models import Flow, DailyFlowRuns


class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = ["uuid", "name", "is_active"]
        read_only_fields = ["is_active"]

    def update(self, instance, validated_data):
        validated_data.pop("uuid")
        return super().update(instance, validated_data)


class DailyFlowRunsSerializer(serializers.ModelSerializer):
    flow = FlowSerializer()

    class Meta:
        model = DailyFlowRuns
        fields = ["flow", "active", "completed", "interrupted", "expired", "day"]


class MostAccessedFlowStatusSerializer(serializers.Serializer):
    uuid = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    active = serializers.IntegerField()
    completed = serializers.IntegerField()
    interrupted = serializers.IntegerField()
    expired = serializers.IntegerField()
