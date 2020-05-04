from rest_framework.permissions import BasePermission


class IsSelfUser(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return request.user == obj


class IsAdminOrSelfUser(IsSelfUser):
    def has_object_permission(self, request, view, obj) -> bool:
        is_self_user: bool = super().has_object_permission(request, view, obj)
        return is_self_user or request.user.is_staff
