from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import UserSerializer, ChangePasswordSerializer
from ..utils.permissions import IsSelfUser, IsAdminOrSelfUser
from ..utils.views import MixedPermissionModelViewSet


class UserViewSet(MixedPermissionModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ["username", "email", "first_name", "is_staff", "is_superuser", "is_active"]
    search_fields = ["username", "email", "first_name"]
    ordering_fields = ["username", "email", "first_name", "is_staff", "is_superuser", "is_active", "date_joined"]
    ordering = ["date_joined"]

    permission_classes_by_action = {
        "create": [IsAdminUser],
        "update": [IsAdminOrSelfUser],
        "partial_update": [IsAdminOrSelfUser],
        "destroy": [IsAdminUser],
    }

    @action(methods=["put"], detail=True, permission_classes=[IsSelfUser])
    def change_password(self, request, pk=None):
        instance = self.get_object()
        serializer = ChangePasswordSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.set_password(serializer.validated_data.get("new_password"))
        instance.save()

        return Response({"message": f"{instance.username} password was changed"})

    @action(methods=["put"], detail=True, permission_classes=[IsAdminUser])
    def change_permission(self, request, pk=None):
        instance = self.get_object()
        instance.is_staff = not instance.is_staff
        instance.save()

        return Response({"message": f"{instance.username} permission has been changed"})

    def perform_destroy(self, instance):
        """Soft delete."""
        instance.is_active = False
        instance.save()
