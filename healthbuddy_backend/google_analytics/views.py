from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .request_formatter import FormatRequestGoogleAnalyticsAPI
from .util import get_results_ga, get_results_mcf, get_results_realtime

from rest_framework_simplejwt.authentication import JWTAuthentication

from healthbuddy_backend.utils.authentication import QueryParamsFixedTokenAuthentication, \
    HeaderFixedTokenAuthentication


class GAGoogleAnalyticsAPIView(ListAPIView):
    """Get the google analytics data (Google Analytics) from the registered account"""

    authentication_classes = (HeaderFixedTokenAuthentication, JWTAuthentication)

    def get(self, request, *args, **kwargs):
        cleaner_request = FormatRequestGoogleAnalyticsAPI("ga", request)
        query_params_cleaned = cleaner_request.get_params_formated()

        try:
            result = get_results_ga(**query_params_cleaned)
        except Exception as e:
            message_error = str(e).replace("get_results_ga() ", "")
            return Response({"message": message_error}, 400)

        return Response(result, 200)


class MCFGoogleAnalyticsAPIView(ListAPIView):
    """Get the google analytics data (Multi-Channel Funnels) from the registered account"""

    def get(self, request, *args, **kwargs):
        cleaner_request = FormatRequestGoogleAnalyticsAPI("mcf", request)
        query_params_cleaned = cleaner_request.get_params_formated()

        try:
            result = get_results_mcf(**query_params_cleaned)
        except Exception as e:
            message_error = str(e).replace("get_results_mcf() ", "")
            return Response({"message": message_error}, 400)

        return Response(result, 200)


class RealTimeGoogleAnalyticsAPIView(ListAPIView):
    """Get the google analytics data (Real Time) from the registered account"""

    def get(self, request, *args, **kwargs):
        cleaner_request = FormatRequestGoogleAnalyticsAPI("rt", request)
        query_params_cleaned = cleaner_request.get_params_formated()

        try:
            result = get_results_realtime(**query_params_cleaned)
        except Exception as e:
            message_error = str(e).replace("get_results_realtime() ", "")
            return Response({"message": message_error}, 400)

        return Response(result, 200)
