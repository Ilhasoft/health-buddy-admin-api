from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .util import get_results_ga, get_results_mcf, get_results_realtime


class FormatRequestGoogleAnalyticsAPI:
    """Cleans up query params to become the standard accepted by the google analytics API."""

    def __init__(self, prefix, request):
        self._prefix = prefix
        self._request = request

    def _format_query_param_with_prefix(self, query_param_value: str):
        """Converts a comma-separated list to a string with all values formatted with the prefix."""

        if not query_param_value:
            return None

        values_param: list = query_param_value.split(",")

        formated_param_values = ""
        for value in values_param:
            formated_param_values += f",{self._prefix}:{value}"

        formated_param_values: str = formated_param_values[1:]  # removes the first element because it is an unwanted comma

        return formated_param_values

    def _clean_query_params(self) -> dict:
        """
        Converts a QueryDict to a dict and takes the values of that dict from within an array and transforms it
        into a string.
        """

        new_query_params = {}
        query_params = dict(self._request.query_params)
        for key, value in query_params.items():
            new_query_params[key] = value.pop(0)

        return new_query_params

    def get_params_formated(self) -> dict:
        """Returns a query params dictionary ready to be used in the google analytics api."""

        query_params_cleaned: dict = self._clean_query_params()
        new_metrics: str = self._format_query_param_with_prefix(
            query_params_cleaned.get("metrics")
        )
        new_dimensions: str = self._format_query_param_with_prefix(
            query_params_cleaned.get("dimensions")
        )
        query_params_cleaned["metrics"] = new_metrics
        query_params_cleaned["dimensions"] = new_dimensions

        return query_params_cleaned


class GAGoogleAnalyticsAPIView(ListAPIView):
    """Get the google analytics data (Google Analytics) from the registered account"""

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
