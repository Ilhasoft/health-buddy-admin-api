from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .models import FakeNews
from ..utils.base_test import AuthenticationTestTemplate


class FakeNewsListTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.get

    def _get_basename_url(self):
        return "fakenews-list"

    def _get_kwargs_url(self):
        return {}

    def test_action_user_without_permission(self):
        """all logged user has permission."""
        pass

    def test_list_10_obj_paginated_token(self):
        fakenews = []
        user = self.create_normal_user("author")
        for i in range(0, 11):
            fakenews.append(
                FakeNews(
                    author=user,
                    title=f"test create fakenews title{i}",
                    subtitle=f"test create fakenews subtitle{i}",
                    body=f"test create fakenews body{i}",
                )
            )
        FakeNews.objects.bulk_create(fakenews)

        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._make_request()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data.get("results")), 10)
        self.assertEqual(resp.data.get("count"), 11)
        self.assertIsNotNone(resp.data.get("next"))


class FakeNewsDetailTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.get

    def _get_basename_url(self):
        return "fakenews-detail"

    def _get_kwargs_url(self):
        return {"slug": "test-create-fakenews-title"}

    def test_action_user_without_permission(self):
        """all logged user has permission."""
        pass

    def test_detail_obj_token(self):
        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")

        fakenews = FakeNews.objects.create(
            author=User.objects.last(),
            title="test create fakenews title",
            subtitle="test create fakenews subtitle",
            body="test create fakenews body",
        )
        resp = self._client.get(reverse_lazy("fakenews-detail", kwargs={"slug": fakenews.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("title"), fakenews.title)

    def test_detail_not_found(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._client.get(reverse_lazy("fakenews-detail", kwargs={"slug": "slug-not-found"}))
        self.assertEqual(resp.status_code, 404)


class FakeNewsCreateTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.post

    def _get_basename_url(self):
        return "fakenews-list"

    def _get_kwargs_url(self):
        return {}

    def test_action_user_without_permission(self):
        """all logged user has permission."""
        pass

    def test_create_successful(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._client.post(
            reverse_lazy("fakenews-list"),
            data={
                "title": "test create fakenews title",
                "subtitle": "test create fakenews subtitle",
                "body": "test create fakenews body",
            },
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(FakeNews.objects.last().slug, resp.data.get("slug"))

    def test_create_already_exists(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")

        FakeNews.objects.create(
            author=User.objects.last(),
            title="test create fakenews title",
            subtitle="test create fakenews subtitle",
            body="test create fakenews body",
        )
        resp = self._client.post(
            reverse_lazy("fakenews-list"),
            data={
                "title": "test create fakenews title",
                "subtitle": "test create fakenews subtitle",
                "body": "test create fakenews body",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data.get("title").pop(0), "fake news with this title already exists.")

    def test_create_without_fields_required(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._make_request()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data.get("title").pop(0), "This field is required.")


class FakeNewsDeleteTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.delete

    def _get_basename_url(self):
        return "fakenews-detail"

    def _get_kwargs_url(self):
        return {"slug": "test-create-fakenews-title"}

    def test_action_user_without_permission(self):
        """all logged user has permission."""
        pass

    def test_delete_successful(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")

        fakenews = FakeNews.objects.create(
            author=User.objects.last(),
            title="test create fakenews title",
            subtitle="test create fakenews subtitle",
            body="test create fakenews body",
        )
        resp = self._client.delete(reverse_lazy("fakenews-detail", kwargs={"slug": fakenews.slug}))
        self.assertEqual(resp.status_code, 204)


class FakeNewsPatchTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.patch

    def _get_basename_url(self):
        return "fakenews-detail"

    def _get_kwargs_url(self):
        return {"slug": "test-create-fakenews-title"}

    def test_action_user_without_permission(self):
        """all logged user has permission."""
        pass

    def test_patch_normal_user(self):
        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")

        fakenews = FakeNews.objects.create(
            author=User.objects.last(),
            title="test create fakenews title",
            subtitle="test create fakenews subtitle",
            body="test create fakenews body",
        )
        resp = self._client.patch(
            reverse_lazy("fakenews-detail", kwargs={"slug": fakenews.slug}),
            data={"title": "title updated", "subtitle": "subtitle updated", "body": "body updated"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("title"), "title updated")
        self.assertEqual(resp.data.get("slug"), "title-updated")
        self.assertEqual(FakeNews.objects.last().slug, "title-updated")


class FakeNewsUpdateTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.put

    def _get_basename_url(self):
        return "fakenews-detail"

    def _get_kwargs_url(self):
        return {"slug": "test-create-fakenews-title"}

    def test_action_user_without_permission(self):
        """all logged user has permission."""
        pass

    def test_update_normal_user(self):
        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")

        fakenews = FakeNews.objects.create(
            author=User.objects.last(),
            title="test create fakenews title",
            subtitle="test create fakenews subtitle",
            body="test create fakenews body",
        )
        resp = self._client.put(
            reverse_lazy("fakenews-detail", kwargs={"slug": fakenews.slug}),
            data={"title": "title updated", "subtitle": "subtitle updated", "body": "body updated"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("title"), "title updated")
        self.assertEqual(resp.data.get("slug"), "title-updated")
        self.assertEqual(FakeNews.objects.last().slug, "title-updated")


# way to turn a test case class into an abstract
del AuthenticationTestTemplate
