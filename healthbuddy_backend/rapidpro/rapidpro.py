import requests
from django.conf import settings
from rest_framework.request import Request


RAPID_PRO_URL = "https://rapidpro.ilhasoft.mobi/api/v2/{}.json"


def get_flow(flow_uuid=""):
    http_method = "get"
    url = RAPID_PRO_URL.format("flows")
    params = {"uuid": flow_uuid}
    headers = {"Authorization": f"Token {settings.TOKEN_ORG_RAPIDPRO}"}
    response = requests.request(http_method, url, params=params, headers=headers)

    return response.json()


class ProxyRapidPro:
    """
    Turns the request into a RapidPro Request

    :param request: current request made to your endpoint
    """

    def __init__(self, request):
        self.request: Request = request
        self.base_url: str = RAPID_PRO_URL
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
