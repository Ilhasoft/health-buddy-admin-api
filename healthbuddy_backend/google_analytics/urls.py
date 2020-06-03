from django.urls import path

from .views import GAGoogleAnalyticsAPIView, MCFGoogleAnalyticsAPIView, RealTimeGoogleAnalyticsAPIView

urlpatterns = [
    path("ga", GAGoogleAnalyticsAPIView.as_view(), name="ga"),
    path("mcf", MCFGoogleAnalyticsAPIView.as_view(), name="mcf"),
    path("realtime", RealTimeGoogleAnalyticsAPIView.as_view(), name="realtime"),
]
