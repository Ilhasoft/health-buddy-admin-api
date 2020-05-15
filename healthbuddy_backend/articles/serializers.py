from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        read_only_fields = ("id", "author", "slug", "created_on", "modified_on")
        fields = ["url", "id", "author", "title", "slug", "subtitle", "body", "published", "created_on", "modified_on"]
        extra_kwargs = {
            "url": {"view_name": "article-detail", "lookup_field": "slug"},
            "author": {"view_name": "user-detail", "lookup_field": "pk"},
        }
