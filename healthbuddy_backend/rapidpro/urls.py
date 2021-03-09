from django.urls import path

from .views import (
    RapidProProxyView,
    RunsDataListView,
    MostAccessedFlowStatus,
    DailyFlowRunsListView,
    DailyGroupCountListView,
    DailyChannelCountListView,
    LabelMessageCountView,
)

urlpatterns = [
    path("proxy/<str:resource>", RapidProProxyView.as_view(), name="proxy_rapidpro"),
    path("runs/", RunsDataListView.as_view(), name="runs_data_list"),
    path("runs/most_accessed/<str:attribute>", MostAccessedFlowStatus.as_view(), name="flow_most_accessed"),
    path("runs/all/", DailyFlowRunsListView.as_view(), name="daily_flow_runs"),
    path("groups_count/", DailyGroupCountListView.as_view(), name="daily_group_counts"),
    path("channels_count/", DailyChannelCountListView.as_view(), name="daily_channel_counts"),
    path("labels_count/", LabelMessageCountView.as_view(), name="label_counts"),
]
