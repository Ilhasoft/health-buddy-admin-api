from rest_framework import serializers

from .models import Polls


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polls
        fields = ["id","author", "name", "link", "is_active"]
        read_only_fields = ["id", "author"]

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)