from django.urls import path

from ..proxy.views import RapidProProxyView, RapidProTokenView

urlpatterns = [
    path("rapidpro/token", RapidProTokenView.as_view(), name="token_rapidpro"),
    path("rapidpro/<str:resource>", RapidProProxyView.as_view(), name="proxy_rapidpro"),
]
