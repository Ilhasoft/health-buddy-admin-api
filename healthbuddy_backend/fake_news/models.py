from ..posts.models import TextPost


class FakeNews(TextPost):
    class Meta:
        default_related_name = "fakenews"
        ordering = ["created_on"]
