from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .models import Article
from ..utils.base_test import AuthenticationTestTemplate


class ArticleListTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.get

    def _get_basename_url(self):
        return "article-list"

    def _get_kwargs_url(self):
        return {}

    def test_action_user_without_permission(self):
        """all logged user has permission."""
        pass

    def test_list_10_obj_paginated_token(self):
        articles = []
        user = self.create_normal_user("author")
        for i in range(0, 11):
            articles.append(
                Article(
                    author=user,
                    title=f"test create article title{i}",
                    subtitle=f"test create article subtitle{i}",
                    body=f"test create article body{i}",
                )
            )
        Article.objects.bulk_create(articles)

        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._make_request()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data.get("results")), 10)
        self.assertEqual(resp.data.get("count"), 11)
        self.assertIsNotNone(resp.data.get("next"))


class ArticleDetailTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.get

    def _get_basename_url(self):
        return "article-detail"

    def _get_kwargs_url(self):
        return {"slug": "test-create-article-title"}

    def test_action_user_without_permission(self):
        """all logged user has permission."""
        pass

    def test_detail_obj_token(self):
        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")

        article = Article.objects.create(
            author=User.objects.last(),
            title="test create article title",
            subtitle="test create article subtitle",
            body="test create article body",
        )
        resp = self._client.get(reverse_lazy("article-detail", kwargs={"slug": article.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("title"), article.title)

    def test_detail_not_found(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._client.get(reverse_lazy("article-detail", kwargs={"slug": "slug-not-found"}))
        self.assertEqual(resp.status_code, 404)


class ArticleCreateTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.post

    def _get_basename_url(self):
        return "article-list"

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
            reverse_lazy("article-list"),
            data={
                "title": "test create article title",
                "subtitle": "test create article subtitle",
                "body": "test create article body",
            },
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Article.objects.last().slug, resp.data.get("slug"))

    def test_create_already_exists(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")

        Article.objects.create(
            author=User.objects.last(),
            title="test create article title",
            subtitle="test create article subtitle",
            body="test create article body",
        )
        resp = self._client.post(
            reverse_lazy("article-list"),
            data={
                "title": "test create article title",
                "subtitle": "test create article subtitle",
                "body": "test create article body",
            },
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data.get("title").pop(0), "article with this title already exists.")

    def test_create_without_fields_required(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._make_request()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data.get("title").pop(0), "This field is required.")


class ArticleDeleteTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.delete

    def _get_basename_url(self):
        return "article-detail"

    def _get_kwargs_url(self):
        return {"slug": "test-create-article-title"}

    def test_action_user_without_permission(self):
        """all logged user has permission."""
        pass

    def test_delete_successful(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")

        article = Article.objects.create(
            author=User.objects.last(),
            title="test create article title",
            subtitle="test create article subtitle",
            body="test create article body",
        )
        resp = self._client.delete(reverse_lazy("article-detail", kwargs={"slug": article.slug}))
        self.assertEqual(resp.status_code, 204)


class ArticlePatchTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.patch

    def _get_basename_url(self):
        return "article-detail"

    def _get_kwargs_url(self):
        return {"slug": "test-create-article-title"}

    def test_action_user_without_permission(self):
        """all logged user has permission."""
        pass

    def test_patch_normal_user(self):
        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")

        article = Article.objects.create(
            author=User.objects.last(),
            title="test create article title",
            subtitle="test create article subtitle",
            body="test create article body",
        )
        resp = self._client.patch(
            reverse_lazy("article-detail", kwargs={"slug": article.slug}),
            data={"title": "title updated", "subtitle": "subtitle updated", "body": "body updated"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("title"), "title updated")
        self.assertEqual(resp.data.get("slug"), "title-updated")
        self.assertEqual(Article.objects.last().slug, "title-updated")


class ArticleUpdateTestCase(AuthenticationTestTemplate):
    def _get_callable_client_method_http(self):
        return self._client.put

    def _get_basename_url(self):
        return "article-detail"

    def _get_kwargs_url(self):
        return {"slug": "test-create-article-title"}

    def test_action_user_without_permission(self):
        """all logged user has permission."""
        pass

    def test_update_normal_user(self):
        tokens = self.get_token_valid_normal_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")

        article = Article.objects.create(
            author=User.objects.last(),
            title="test create article title",
            subtitle="test create article subtitle",
            body="test create article body",
        )
        resp = self._client.put(
            reverse_lazy("article-detail", kwargs={"slug": article.slug}),
            data={"title": "title updated", "subtitle": "subtitle updated", "body": "body updated"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.get("title"), "title updated")
        self.assertEqual(resp.data.get("slug"), "title-updated")
        self.assertEqual(Article.objects.last().slug, "title-updated")


# way to turn a test case class into an abstract
del AuthenticationTestTemplate
