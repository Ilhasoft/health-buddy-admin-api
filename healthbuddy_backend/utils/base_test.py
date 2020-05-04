import random
import string
from abc import ABCMeta, abstractmethod

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APIClient

from ..utils.messages_tests import RESP_WITHOUT_TOKEN, RESP_DONT_HAVE_PERMISSION, RESP_WRONG_TOKEN


def username_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for x in range(size))


class UserMixin:
    password = "123456789"

    @staticmethod
    def create_user(username, **kwargs) -> User:
        return User.objects.create_user(
            username=username,
            password=kwargs.get("password", UserMixin.password),
            email=kwargs.get("email", "mail@mail.com"),
            first_name=kwargs.get("first_name", "user"),
            last_name=kwargs.get("last_name", "test"),
            is_staff=kwargs.get("is_staff", False),
        )

    def create_admin_user(self, username, **kwargs) -> User:
        kwargs["is_staff"] = True
        return UserMixin.create_user(username=username, **kwargs)

    def create_normal_user(self, username, **kwargs) -> User:
        kwargs["is_staff"] = False
        return UserMixin.create_user(username, **kwargs)


class AuthenticationBaseMixin(UserMixin, metaclass=ABCMeta):
    def get_tokens(self, user):
        client = self.get_client()
        resp = client.post(
            reverse_lazy("token_obtain_pair"), {"username": user.username, "password": UserMixin.password}
        )
        return resp

    def get_token_valid_normal_user(self):
        user = self.create_normal_user(username=username_generator())
        tokens = self.get_tokens(user)
        return tokens.data

    def get_token_valid_admin_user(self):
        user = self.create_admin_user(username=username_generator())
        tokens = self.get_tokens(user)
        return tokens.data

    def get_expired_token(self):
        # todo: not yet implemented
        tokens = self.get_token_valid_normal_user()
        self.get_client().post(reverse_lazy("token_refresh"), {"refresh": tokens.get("refresh")})
        token_acess = tokens.get("access")

        return token_acess

    def get_token_invalid(self):
        return "invalidtoken.verysad"

    @abstractmethod
    def get_client(self):
        ...


class AuthenticationTestTemplate(AuthenticationBaseMixin, TestCase, metaclass=ABCMeta):
    def setUp(self):
        self._client = self.get_client()

    @abstractmethod
    def _get_callable_client_method_http(self):
        ...

    @abstractmethod
    def _get_basename_url(self):
        ...

    @abstractmethod
    def _get_kwargs_url(self):
        ...

    def _get_url_to_request(self):
        base_name = self._get_basename_url()
        kwargs = self._get_kwargs_url()
        return reverse_lazy(base_name, kwargs=kwargs)

    def _make_request(self):
        url_reversed = self._get_url_to_request()
        function_client_method_http = self._get_callable_client_method_http()
        resp = function_client_method_http(url_reversed)
        return resp

    def get_client(self):
        return APIClient()

    def test_action_user_without_token(self):
        resp = self._make_request()
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.data, RESP_WITHOUT_TOKEN)

    def test_action_user_wrong_token(self):
        invalid_token = self.get_token_invalid()
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {invalid_token}")

        resp = self._make_request()

        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.data, RESP_WRONG_TOKEN)

    def test_action_user_without_permission(self):
        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")

        resp = self._make_request()

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.data, RESP_DONT_HAVE_PERMISSION)
