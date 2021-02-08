from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


class QueryParamsFixedTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):

        token = request.query_params.get("token")
        if token != settings.FIXED_REST_TOKEN:
            raise exceptions.AuthenticationFailed("Invalid Token")

        return (AnonymousUser(), None)


class HeaderFixedTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):

        header_token = request.headers.get("Authorization")

        if not self.is_valid_token(header_token):
            raise exceptions.AuthenticationFailed(("Invalid Token"))

        return AnonymousUser(), header_token

    def is_valid_token(self, token: str) -> bool:
        valid_token = f"Bearer {settings.FIXED_REST_TOKEN}"

        if token == valid_token:
            return True

        return False
