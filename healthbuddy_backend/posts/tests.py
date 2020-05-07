import io
import os

from PIL import Image
from django.conf import settings

from rest_framework.reverse import reverse_lazy

from ..utils.base_test import AuthenticationTestTemplate
from .models import Image as ImageModel


def generate_image():
    file = io.BytesIO()
    image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
    image.save(file, "png")
    file.name = "test.png"
    file.seek(0)
    return file


class UploadImageCreateTestCase(AuthenticationTestTemplate):
    def tearDown(self):
        image_instance_db = ImageModel.objects.last()
        if image_instance_db:
            file = os.path.join(settings.MEDIA_ROOT, f"{image_instance_db.image}")
            os.remove(file)

    def _get_callable_client_method_http(self):
        return self._client.post

    def _get_basename_url(self):
        return "upload_image_post"

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
            reverse_lazy(self._get_basename_url()), data={"image": generate_image()}, format="multipart"
        )
        self.assertEqual(resp.status_code, 201)
        self.assertIn("image", resp.data)
        self.assertEqual(ImageModel.objects.count(), 1)
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, f"{ImageModel.objects.last().image}")))

    def test_create_without_fields_required(self):
        tokens = self.get_token_valid_admin_user()
        token_access = tokens.get("access")
        self._client.credentials(HTTP_AUTHORIZATION=f" Bearer {token_access}")
        resp = self._make_request()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data.get("image").pop(0), "No file was submitted.")


# way to turn a test case class into an abstract
del AuthenticationTestTemplate
