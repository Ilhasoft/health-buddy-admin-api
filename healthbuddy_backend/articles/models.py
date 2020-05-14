from ..posts.models import TextPost


class Article(TextPost):
    class Meta:
        default_related_name = "articles"
        ordering = ["created_on"]
