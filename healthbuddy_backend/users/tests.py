from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client
from django.db.models import Q
from django.urls import reverse


class BaseManagementUserTestCase(TestCase):
    def _login_required(self, url_namespace, **kwargs):
        url = reverse(url_namespace, **kwargs)
        self.client.logout()
        resp = self.client.get(url, {})
        self.assertRedirects(resp, "/login/?next=" + url)

    def _permission_required(self, url_namespace, **kwargs):
        url = reverse(url_namespace, **kwargs)
        self.client.login(username="normaluser", password="normaluser")
        resp = self.client.get(url, {})
        self.assertEqual(resp.status_code, 403)

    def _create_users(self):
        self.normal_user = User.objects.create(username="normaluser", email="mail@mail.com")
        self.normal_user.set_password("normaluser")
        self.normal_user.save()

        self.user_manager = User.objects.create(username="manageruser", email="mail@mail.com")
        self.user_manager.set_password("manageruser")
        self.user_manager.save()

        self._set_management_user_permissions()

    def _set_management_user_permissions(self):
        permissions = list(
            Permission.objects.filter(
                Q(codename="add_user") |
                Q(codename="change_user") |
                Q(codename="delete_user")
            )
        )
        self.user_manager.user_permissions.set(permissions)
        self.user_manager.save()

    def setUp(self):
        self._create_users()
        self.client = Client()

    class Meta:
        abstract = True


class UserListTestCase(BaseManagementUserTestCase):
    def test_list_view_login_required(self):
        self._login_required("list_user")


class UserAddTestCase(BaseManagementUserTestCase):
    def setUp(self):
        self.url_namespace = "add_user"
        self.url = reverse(self.url_namespace)
        self.form_data = {
            "username": "testing",
            "first_name": "test",
            "last_name": "ing",
            "email": "mail@mail.com",
            "password1": "ABC@123456",
            "password2": "ABC@123456"
        }
        super().setUp()

    def test_add_view_login_required(self):
        self._login_required(self.url_namespace)

    def test_add_view_permission_required(self):
        self._permission_required(self.url_namespace)

    def test_create_user_successful(self):
        self.client.login(username="manageruser", password="manageruser")
        resp = self.client.post(self.url, self.form_data)
        self.assertEqual(User.objects.last().username, "testing")
        self.assertRedirects(resp, reverse("list_user"))

    def test_create_user_fail(self):
        self.client.login(username="manageruser", password="manageruser")
        self.form_data["password1"] = "passwordsdontmatch"
        self.client.post(self.url, {})
        self.client.post(self.url, self.form_data)
        self.assertEqual(User.objects.all().count(), 2)


class UserDetailTestCase(BaseManagementUserTestCase):
    def test_detail_view_login_required(self):
        self._login_required("detail_user", kwargs={"pk": self.user_manager.pk})


class UserUpdateTestCase(BaseManagementUserTestCase):
    def test_update_view_login_required(self):
        self._login_required("update_user", kwargs={"pk": self.user_manager.pk})

    def test_update_view_permission_required(self):
        self._permission_required("update_user", kwargs={"pk": self.user_manager.pk})


class UserAccessManagementTestCase(BaseManagementUserTestCase):
    def test_access_management_view_login_required(self):
        self._login_required("delete_user", kwargs={"pk": self.user_manager.pk})

    def test_update_view_permission_required(self):
        self._permission_required("delete_user", kwargs={"pk": self.user_manager.pk})
