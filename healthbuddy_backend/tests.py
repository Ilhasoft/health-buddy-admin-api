from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class UserAuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", email="mail@mail.com")
        self.user.set_password("password_correct")
        self.user.save()

        self.client = Client()

    def test_login_fail(self):
        fail_login_password = self.client.login(username="test", password="password_wrong")
        fail_login_username = self.client.login(username="test_wrong", password="password_correct")
        self.assertFalse(fail_login_password)
        self.assertFalse(fail_login_username)

    def test_login_success(self):
        success_login = self.client.login(username="test", password="password_correct")
        self.assertTrue(success_login)
