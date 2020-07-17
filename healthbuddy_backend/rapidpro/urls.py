from django.urls import path

from .views import RapidProProxyView

urlpatterns = [
    path("proxy/<str:resource>", RapidProProxyView.as_view(), name="proxy_rapidpro"),
]
