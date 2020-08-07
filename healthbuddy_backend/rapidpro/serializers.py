from rest_framework import serializers

from .models import Flow


class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = ["uuid", "name", "active"]
        read_only_fields = ["active"]

    def update(self, instance, validated_data):
        validated_data.pop("uuid")
        return super().update(instance, validated_data)


class MostAccessedFlowStatusSerializer(serializers.Serializer):
    uuid = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    active = serializers.IntegerField()
    completed = serializers.IntegerField()
    interrupted = serializers.IntegerField()
    expired = serializers.IntegerField()
