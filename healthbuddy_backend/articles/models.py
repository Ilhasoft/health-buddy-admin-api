from ..posts.models import TextPost


class Article(TextPost):
    class Meta:
        ordering = ["created_on"]
