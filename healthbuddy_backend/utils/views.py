from typing import List

from rest_framework import viewsets
from rest_framework.permissions import BasePermission


class MixedPermissionModelViewSet(viewsets.ModelViewSet):
    """Mixed permission base model allowing for action level
    permission control. Subclasses may define their permissions
    by creating a 'permission_classes_by_action' variable.

    Example:
    permission_classes_by_action = {'list': [AllowAny],
                                   'create': [IsAdminUser]}

    solution by:
    https://stackoverflow.com/questions/35970970/django-rest-
    framework-permission-classes-of-viewset-method
    """

    permission_classes_by_action = {}

    def get_permissions(self) -> List[BasePermission]:
        """Returns as permissions of an HTTP method."""
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
