from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, unique=True)
    slug = AutoSlugField(max_length=120, unique=True, always_update=True, populate_from="title")
    subtitle = models.CharField(max_length=255)
    published = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TextPost(Post):
    body = models.TextField()

    class Meta:
        abstract = True


class Image(models.Model):
    image = models.ImageField(upload_to="posts/")
