from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .util import get_results_ga, get_results_mcf, get_results_realtime


class GAGoogleAnalyticsAPIView(ListAPIView):
    def get(self, request, *args, **kwargs):
        query_params = dict(request.query_params)
        result = get_results_ga(**query_params)
        return Response(result, 200)


class MCFGoogleAnalyticsAPIView(ListAPIView):
    def get(self, request, *args, **kwargs):
        query_params = dict(request.query_params)
        result = get_results_mcf(**query_params)
        return Response(result, 200)


class RealTimeGoogleAnalyticsAPIView(ListAPIView):
    def get(self, request, *args, **kwargs):
        query_params = dict(request.query_params)
        result = get_results_realtime(**query_params)
        return Response(result, 200)
