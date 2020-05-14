from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from .models import Video
from .serializers import VideoSerializer


class VideoViewSet(viewsets.ModelViewSet):
    parser_classes = (
        FormParser,
        MultiPartParser,
    )
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = "slug"
    filterset_fields = ["author", "title", "slug", "subtitle", "published", "created_on", "modified_on"]
    search_fields = ["author", "title", "slug", "subtitle"]
    ordering_fields = ["author", "title", "slug", "subtitle", "published", "created_on", "modified_on"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
