import requests
from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .rapidpro import ProxyRapidPro


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
