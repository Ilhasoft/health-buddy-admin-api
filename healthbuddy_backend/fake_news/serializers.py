from rest_framework import serializers

from .models import FakeNews


class FakeNewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FakeNews
        read_only_fields = ("author", "slug", "created_on", "modified_on")
        fields = ["url", "author", "title", "slug", "subtitle", "body", "published", "created_on", "modified_on"]
        extra_kwargs = {
            "url": {"view_name": "fakenews-detail", "lookup_field": "slug"},
            "author": {"view_name": "user-detail", "lookup_field": "pk"},
        }
