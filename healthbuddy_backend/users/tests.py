from django.contrib.auth.models import User
from django.urls import reverse_lazy

from ..utils.base_test import AuthenticationTestTemplate
from ..utils.messages_tests import USER_CREATE_PASSWORD_LESS_THAN_8, USER_CREATE_REQUIRED_FIELDS, USER_ALREADY_EXISTS


class UserListTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.get

    def _get_basename_url(self):
        return "user-list"

    def _get_kwargs_url(self):
        return {}

    def test_list_10_obj_paginated_token(self):
        for i in range(0, 10):
            self.create_normal_user(username=f"test{i}")

        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._make_request()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data.get("results")), 10)
        self.assertEqual(resp.data.get("count"), 11)
        self.assertIsNotNone(resp.data.get("next"))


class UserDetailTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.get

    def _get_basename_url(self):
        return "user-detail"

    def _get_kwargs_url(self):
        return {"pk": 1}

    def test_detail_obj_token(self):
        user = self.create_normal_user(username="test")
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._client.get(reverse_lazy("user-detail", kwargs={"pk": user.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("username"), user.username)

    def test_detail_not_found(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._client.get(reverse_lazy("user-detail", kwargs={"pk": 1000}))
        self.assertEqual(resp.status_code, 404)


class UserCreateTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.post

    def _get_basename_url(self):
        return "user-list"

    def _get_kwargs_url(self):
        return {}

    def test_create_successful(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._client.post(
            reverse_lazy("user-list"),
            data={
                "username": "test_create",
                "password": "testcreate",
                "email": "mail@mail.com",
                "first_name": "test",
                "last_name": "create",
            },
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(User.objects.last().username, resp.data.get("username"))

    def test_create_already_exists(self):
        self.create_normal_user(username="test_create")
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._client.post(
            reverse_lazy("user-list"),
            data={
                "username": "test_create",
                "password": "testcreate",
                "email": "mail@mail.com",
                "first_name": "test",
                "last_name": "create",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data, USER_ALREADY_EXISTS)

    def test_create_without_fields_required(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._make_request()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data, USER_CREATE_REQUIRED_FIELDS)

    def test_create_user_with_password_less_than_8_characters(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._client.post(reverse_lazy("user-list"), data={"username": "test_password", "password": "123456"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data, USER_CREATE_PASSWORD_LESS_THAN_8)


class UserDeleteTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.delete

    def _get_basename_url(self):
        return "user-detail"

    def _get_kwargs_url(self):
        return {"pk": 1}

    def test_delete_successful(self):
        user = self.create_normal_user(username="usertobedeleted")
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._client.delete(reverse_lazy("user-detail", kwargs={"pk": user.pk}))
        self.assertEqual(resp.status_code, 204)


class UserActiveTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.patch

    def _get_basename_url(self):
        return "user-active-user"

    def _get_kwargs_url(self):
        return {"pk": 1}

    def test_active_successful(self):
        user = self.create_normal_user(username="usertobeactivate")
        user.is_active = False
        user.save()
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._client.patch(reverse_lazy("user-active-user", kwargs={"pk": user.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("message"), f"{user.username} user has been activated!")
        self.assertTrue(User.objects.get(pk=user.pk).is_active)


class UserChangePermissionTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.put

    def _get_basename_url(self):
        return "user-change-permission"

    def _get_kwargs_url(self):
        return {"pk": 1}

    def test_change_permission_successful(self):
        user = self.create_normal_user(username="userchangepermission")
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._client.put(reverse_lazy("user-change-permission", kwargs={"pk": user.pk}))
        self.assertEqual(resp.status_code, 200)


class UserChangePasswordTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.put

    def _get_basename_url(self):
        return "user-change-password"

    def _get_kwargs_url(self):
        user = self.create_normal_user("usertochangepassword")
        return {"pk": user.pk}

    def test_change_password_successful(self):
        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        user = User.objects.last()
        resp = self._client.put(
            reverse_lazy("user-change-password", kwargs={"pk": user.pk}),
            data={"current_password": "123456789", "new_password": "newpassword"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(User.objects.last().check_password("newpassword"))

    def test_fields_obrigatory(self):
        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        user = User.objects.last()
        resp = self._client.put(reverse_lazy("user-change-password", kwargs={"pk": user.pk}),)
        self.assertEqual(resp.status_code, 400)
        self.assertIsNotNone(resp.data.get("current_password"))
        self.assertIsNotNone(resp.data.get("new_password"))


class UserPatchTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.patch

    def _get_basename_url(self):
        return "user-detail"

    def _get_kwargs_url(self):
        user = self.create_normal_user("patchuser")
        return {"pk": user.pk}

    def test_patch_normal_user(self):
        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        user = User.objects.last()
        resp = self._client.patch(
            reverse_lazy("user-detail", kwargs={"pk": user.pk}),
            data={
                "username": "userupdated",
                "email": "emailchanged@mail.com",
                "first_name": "firstnamechanged",
                "last_name": "lastnamechanged",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("username"), "userupdated")
        self.assertEqual(User.objects.last().username, "userupdated")

    def test_admin_patch_normal_user(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        user = self.create_normal_user("usereditedbyadmin")
        resp = self._client.patch(
            reverse_lazy("user-detail", kwargs={"pk": user.pk}),
            data={
                "username": "userupdated",
                "email": "emailchanged@mail.com",
                "first_name": "firstnamechanged",
                "last_name": "lastnamechanged",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("username"), "userupdated")
        self.assertEqual(User.objects.last().username, "userupdated")


class UserUpdateTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.put

    def _get_basename_url(self):
        return "user-detail"

    def _get_kwargs_url(self):
        user = self.create_normal_user("userupdate")
        return {"pk": user.pk}

    def test_update_normal_user(self):
        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        user = User.objects.last()
        resp = self._client.put(
            reverse_lazy("user-detail", kwargs={"pk": user.pk}),
            data={
                "username": "userupdated",
                "email": "emailchanged@mail.com",
                "first_name": "firstnamechanged",
                "last_name": "lastnamechanged",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("username"), "userupdated")
        self.assertEqual(User.objects.last().username, "userupdated")

    def test_admin_update_normal_user(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        user = self.create_normal_user("usereditedbyadmin")
        resp = self._client.put(
            reverse_lazy("user-detail", kwargs={"pk": user.pk}),
            data={
                "username": "userupdated",
                "email": "emailchanged@mail.com",
                "first_name": "firstnamechanged",
                "last_name": "lastnamechanged",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("username"), "userupdated")
        self.assertEqual(User.objects.last().username, "userupdated")


class UserMyProfileTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.get

    def _get_basename_url(self):
        return "user-my-profile"

    def _get_kwargs_url(self):
        return {}

    def test_action_user_without_permission(self):
        """all logged user has permission."""
        pass

    def test_my_profile_user(self):
        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        user = User.objects.last()
        resp = self._client.get(reverse_lazy(self._get_basename_url()))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("username"), user.username)


# way to turn a test case class into an abstract
del AuthenticationTestTemplate
