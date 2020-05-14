from rest_framework.generics import CreateAPIView

from .serializers import ImageSerializer


class ImageCreateView(CreateAPIView):
    serializer_class = ImageSerializer
