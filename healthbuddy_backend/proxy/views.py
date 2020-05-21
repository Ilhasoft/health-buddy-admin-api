import requests
from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class ProxyRapidPro:
    """
    Turns the request into a RapidPro Request

    :param request: current request made to your endpoint
    """

    def __init__(self, request):
        self.request: Request = request
        self.base_url: str = "https://rapidpro.ilhasoft.mobi/api/v2/{}.json"
        self.__token: str = settings.TOKEN_ORG_RAPIDPRO

    def __get_headers(self) -> dict:
        return {"Authorization": f"Token {self.__token}"}

    def get_url(self, resource) -> str:
        return self.base_url.format(resource)

    def get_http_method(self) -> str:
        return self.request.method

    def get_params(self) -> dict:
        return self.request.query_params

    def get_data(self) -> dict:
        return self.request.data

    def make_request(self, resource) -> requests.models.Response:
        http_method: str = self.get_http_method()
        url: str = self.get_url(resource)
        params: dict = self.get_params()
        data: dict = self.get_data()
        headers: dict = self.__get_headers()

        return requests.request(http_method, url, params=params, headers=headers, data=data)


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


class RapidProTokenView(ListAPIView):
    """
    Return RapidPro ORG Token
    """

    def get(self, request, *args, **kwargs):
        data = {"token": settings.TOKEN_ORG_RAPIDPRO}

        return Response(data=data, status=200)
