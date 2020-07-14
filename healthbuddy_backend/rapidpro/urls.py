from django.urls import path

from .views import RapidProProxyView, RapidProTokenView

urlpatterns = [
    path("proxy/token", RapidProTokenView.as_view(), name="token_rapidpro"),
    path("proxy/<str:resource>", RapidProProxyView.as_view(), name="proxy_rapidpro"),
]
