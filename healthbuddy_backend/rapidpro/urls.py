from django.urls import path

from .views import RapidProProxyView, RunsDataListView

urlpatterns = [
    path("proxy/<str:resource>", RapidProProxyView.as_view(), name="proxy_rapidpro"),
    path("runs/", RunsDataListView.as_view(), name="runs_data_list"),
]
