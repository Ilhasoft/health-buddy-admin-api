from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        read_only_fields = ("id", "is_staff", "is_active")
        extra_kwargs = {"password": {"write_only": True, "min_length": 8, "required": False}}
        fields = ["url", "id", "username", "password", "email", "first_name", "last_name", "is_staff", "is_active"]

    def get_fields(self):
        fields = super().get_fields()

        request = self.context.get("request")
        if request.method == "POST":
            fields["password"].required = True

        return fields

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("password", None)
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["current_password", "new_password"]

    def validate_current_password(self, value):
        instance = self.instance
        if not instance.check_password(value):
            raise serializers.ValidationError("The current password does not match")

        return value
