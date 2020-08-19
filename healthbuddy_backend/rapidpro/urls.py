from django.urls import path

from .views import RapidProProxyView, RunsDataListView, MostAccessedFlowStatus, DailyFlowRunsListViewSet

urlpatterns = [
    path("proxy/<str:resource>", RapidProProxyView.as_view(), name="proxy_rapidpro"),
    path("runs/", RunsDataListView.as_view(), name="runs_data_list"),
    path("runs/most_accessed/<str:attribute>", MostAccessedFlowStatus.as_view(), name="flow_most_accessed"),
    path("runs/all/", DailyFlowRunsListViewSet.as_view(), name="daily_flow_runs"),
]
