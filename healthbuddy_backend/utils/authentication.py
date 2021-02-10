from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.authentication import BaseAuthentication

from rest_framework_simplejwt import exceptions


class BaseFixedTokenAuthentication(BaseAuthentication):

    def _get_superuser(self):
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            raise exceptions.AuthenticationFailed("No superusers identified")

        return user


class QueryParamsFixedTokenAuthentication(BaseFixedTokenAuthentication):
    def authenticate(self, request):

        token = request.query_params.get("token")
        if token != settings.FIXED_ENDPOINT_TOKEN:
            return None

        return self._get_superuser(), None


class HeaderFixedTokenAuthentication(BaseFixedTokenAuthentication):

    def authenticate(self, request):

        header_token = request.headers.get("Authorization")

        if not self.is_valid_token(header_token):
            return None

        return self._get_superuser(), None

    def is_valid_token(self, token: str) -> bool:
        valid_token = f"Bearer {settings.FIXED_ENDPOINT_TOKEN}"

        if token == valid_token:
            return True

        return False
