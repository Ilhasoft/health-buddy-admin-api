from django.db import models

from ..posts.models import Post


class Video(Post):
    video = models.FileField(blank=False, null=False)
