from rest_framework import viewsets

from .models import FakeNews
from .serializers import FakeNewsSerializer


class FakeNewsViewSet(viewsets.ModelViewSet):
    queryset = FakeNews.objects.all()
    serializer_class = FakeNewsSerializer
    lookup_field = "slug"
    filterset_fields = ["author", "title", "slug", "subtitle", "published", "created_on", "modified_on"]
    search_fields = ["author", "title", "slug", "subtitle"]
    ordering_fields = ["author", "title", "slug", "subtitle", "published", "created_on", "modified_on"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
