from datetime import date
import requests
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Flow, DailyFlowRuns
from .rapidpro import ProxyRapidPro
from .serializers import FlowSerializer, MostAccessedFlowStatusSerializer


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
        sum_results = runs_data.aggregate(
            active=Sum("active"),
            completed=Sum("completed"),
            interrupted=Sum("interrupted"),
            expired=Sum("expired")
        )

        return Response(sum_results, status=200)


class MostAccessedFlowStatus(APIView):
    def get(self, request, attribute):
        flows = Flow.objects.all().annotate(
            active=Sum("runs__active"),
            completed=Sum("runs__completed"),
            interrupted=Sum("runs__interrupted"),
            expired=Sum("runs__expired")
        ).order_by(f"-{attribute}")

        flows_serializer = MostAccessedFlowStatusSerializer(flows, many=True)

        return Response(flows_serializer.data, status=200)
