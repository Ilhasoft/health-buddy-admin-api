from rest_framework import serializers

from .models import Video


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        read_only_fields = ("id", "author", "slug", "created_on", "modified_on")
        fields = [
            "url",
            "id",
            "author",
            "title",
            "slug",
            "subtitle",
            "video",
            "published",
            "created_on",
            "modified_on",
        ]
        extra_kwargs = {
            "url": {"view_name": "video-detail", "lookup_field": "slug"},
            "author": {"view_name": "user-detail", "lookup_field": "pk"},
        }
