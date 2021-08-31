from django.db import models
from django.conf import settings


class Polls(models.Model):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    author = models.CharField(max_length=255)

