import requests
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Flow
from .rapidpro import ProxyRapidPro
from .serializers import FlowSerializer


class RapidProProxyView(ListAPIView):
    """
    Endpoint to transforms the current request into a RapidPro request
    """

    def get(self, request, *args, **kwargs):
        resource: str = kwargs.get("resource")
        proxy = ProxyRapidPro(request)
        response: requests.models.Response = proxy.make_request(resource)

        try:
            data = response.json()
        except Exception as e:
            data = {"message": "An error has occurred!", "error": str(e)}

        return Response(data=data, status=response.status_code)


class FlowViewSet(viewsets.ModelViewSet):
    serializer_class = FlowSerializer
    queryset = Flow.objects.all()
    http_method_names = ["get", "post", "delete"]
