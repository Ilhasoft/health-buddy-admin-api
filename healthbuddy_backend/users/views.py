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
    filterset_fields = ["id", "username", "email", "first_name", "last_name", "is_staff", "is_superuser", "is_active"]
    search_fields = ["id", "username", "email", "first_name", "last_name"]
    ordering_fields = [
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    ]
    ordering = ["date_joined"]

    permission_classes_by_action = {
        "list": [IsAdminUser],
        "retrieve": [IsAdminUser],
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

    @action(methods=["GET"], detail=False)
    def my_profile(self, request):
        user = request.user
        user_serialized = self.get_serializer(user)

        return Response(user_serialized.data)

    @action(methods=["PATCH"], detail=True, permission_classes=[IsAdminUser])
    def active_user(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()

        return Response(data={"message": f"{user.username} user has been activated!"}, status=200)

    def perform_destroy(self, instance):
        """Soft delete."""
        instance.is_active = False
        instance.save()
