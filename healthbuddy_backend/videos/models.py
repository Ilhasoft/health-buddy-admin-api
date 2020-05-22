from django.db import models

from ..posts.models import Post
from ..storage_backends import PublicMediaStorage


class Video(Post):
    video = models.FileField(storage=PublicMediaStorage(), blank=False, null=False)
