import requests
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Flow,
    DailyFlowRuns,
    DailyGroupCount,
    DailyChannelCount,
    Label,
)
from .rapidpro import ProxyRapidPro
from .serializers import (
    FlowSerializer,
    MostAccessedFlowStatusSerializer,
    DailyFlowRunsSerializer,
    DailyGroupCountSerializer,
    DailyChannelCountSerializer,
    LabelCountSerializer,
)
from healthbuddy_backend.utils.authentication import (
    QueryParamsFixedTokenAuthentication,
    HeaderFixedTokenAuthentication,
)
from rest_framework_simplejwt.authentication import JWTAuthentication


class RapidProProxyView(ListAPIView):
    """
    Endpoint to transforms the current request into a RapidPro request
    """

    authentication_classes = (HeaderFixedTokenAuthentication, JWTAuthentication)

    def get(self, request, *args, **kwargs):
        resource: str = kwargs.get("resource")
        proxy = ProxyRapidPro(request)
        response: requests.models.Response = proxy.make_request(resource)

        try:
            data = response.json()
        except Exception as e:
            data = {"message": "An error has occurred!", "error": str(e)}

        return Response(data=data, status=response.status_code)


class FlowViewSet(viewsets.ModelViewSet):
    serializer_class = FlowSerializer
    queryset = Flow.objects.all()
    filterset_fields = ["uuid", "name", "is_active"]
    search_fields = ["uuid", "name", "is_active"]
    ordering_fields = ["uuid", "name", "is_active"]
    http_method_names = ["get", "put", "post", "delete"]

    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()

    @action(methods=["put"], detail=True, permission_classes=[IsAdminUser])
    def active(self, request, pk=None):
        flow = self.get_object()
        flow.is_active = True
        flow.save()

        return Response(data={"message": f"{flow.name} has been activated!"}, status=200)


class RunsDataListView(APIView):

    authentication_classes = (HeaderFixedTokenAuthentication, JWTAuthentication)

    def _get_filters(self, query_params={}):
        filters = {}

        start_date = query_params.get("start_date", "2000-01-01")
        end_date = query_params.get("end_date", "2999-01-01")
        filters["day__range"] = [
            start_date,
            end_date
        ]

        flow = query_params.get("flow")
        if flow:
            filters["flow__uuid"] = flow

        return filters

    def get(self, request):
        query_params = request.query_params
        filters = self._get_filters(query_params)
        runs_data = DailyFlowRuns.objects.all().filter(**filters)

        try:
            last_date = runs_data.last().day.date()
        except AttributeError:
            last_date = None
        flows_last_date = runs_data.filter(day__date=last_date)
        actives_from_flows_last_date = sum(flows_last_date.values_list("active", flat=True))

        sum_results = runs_data.aggregate(
            completed=Coalesce(Sum("completed"), 0),
            interrupted=Coalesce(Sum("interrupted"), 0),
            expired=Coalesce(Sum("expired"), 0)
        )

        sum_results["active"] = actives_from_flows_last_date

        return Response(sum_results, status=200)


class MostAccessedFlowStatus(APIView):

    authentication_classes = (QueryParamsFixedTokenAuthentication, JWTAuthentication)

    def get(self, request, attribute):
        query_params = self.request.query_params
        start_date = query_params.get("start_date", "2000-01-01")
        end_date = query_params.get("end_date", "2100-01-01")
        flows = Flow.objects.all().filter(
            is_active=True,
            runs__day__range=[start_date, end_date]
        ).annotate(
            active=Sum("runs__active"),
            completed=Sum("runs__completed"),
            interrupted=Sum("runs__interrupted"),
            expired=Sum("runs__expired")
        ).order_by(f"-{attribute}")

        flows_serializer = MostAccessedFlowStatusSerializer(flows, many=True)

        return Response(flows_serializer.data, status=200)


class DailyFlowRunsListView(ListAPIView):

    authentication_classes = (HeaderFixedTokenAuthentication, JWTAuthentication)

    queryset = DailyFlowRuns.objects.all()
    model = DailyFlowRuns
    pagination_class = None
    serializer_class = DailyFlowRunsSerializer
    filterset_fields = ["flow__uuid", "flow__name", "day"]
    search_fields = ["flow__uuid", "flow__name", "day"]
    ordering_fields = ["flow__uuid", "flow__name", "day"]

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        start_date = query_params.get("start_date", "2000-01-01")
        end_date = query_params.get("end_date", "2100-01-01")
        queryset = queryset.filter(day__range=[start_date, end_date])
        return super().filter_queryset(queryset).order_by("day")


class DailyGroupCountListView(ListAPIView):

    authentication_classes = (HeaderFixedTokenAuthentication, JWTAuthentication)

    queryset = DailyGroupCount.objects.all()
    model = DailyGroupCount
    pagination_class = None
    serializer_class = DailyGroupCountSerializer
    filterset_fields = ["group__uuid", "group__name", "day"]
    search_fields = ["group__uuid", "group__name", "day"]
    ordering_fields = ["group__uuid", "group__name", "day"]

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        start_date = query_params.get("start_date", "2000-01-01")
        end_date = query_params.get("end_date", "2100-01-01")
        queryset = queryset.filter(day__range=[start_date, end_date])
        return super().filter_queryset(queryset).order_by("day")


class DailyChannelCountListView(ListAPIView):
    queryset = DailyChannelCount.objects.all()
    model = DailyChannelCount
    pagination_class = None
    serializer_class = DailyChannelCountSerializer
    filterset_fields = ["channel__uuid", "channel__name", "day"]
    search_fields = ["channel__uuid", "channel__name", "day"]
    ordering_fields = ["channel__uuid", "channel__name", "day"]

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        start_date = query_params.get("start_date", "2000-01-01")
        end_date = query_params.get("end_date", "2100-01-01")
        queryset = queryset.filter(day__range=[start_date, end_date])
        return super().filter_queryset(queryset).order_by("day")


class LabelMessageCountView(ListAPIView):
    authentication_classes = (HeaderFixedTokenAuthentication, JWTAuthentication)
    queryset = Label.objects.all()
    pagination_class = None
    serializer_class = LabelCountSerializer
    filterset_fields = ["uuid", "name"]
    search_fields = ["uuid", "name"]
    ordering_fields = ["uuid", "name"]

    def get_queryset(self):
        query_params = self.request.query_params
        start_date = query_params.get("start_date", "2000-01-01")
        end_date = query_params.get("end_date", "2100-01-01")

        return self.queryset.annotate(
            msg_count=Count(
                "messages",
                filter=Q(messages__day__range=[start_date, end_date])
            )
        ).order_by("-msg_count")
