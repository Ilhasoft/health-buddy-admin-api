from django.conf import settings
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service():
    """Get a service that communicates to a Google API."""
    scopes = ["https://www.googleapis.com/auth/analytics.readonly"]
    key_file_path = settings.GOOGLE_API_KEY_FILE_PATH
    credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file_path, scopes=scopes)

    return build("analytics", "v3", credentials=credentials)


def get_results_ga(
    start_date: str,
    end_date: str,
    metrics: str,
    filters: str = None,
    sort: str = None,
    include_empty_rows: bool = True,
    segment: str = None,
    output: str = "json",
    max_results: int = None,
    start_index: int = None,
    sampling_level: str = None,
    dimensions: str = None,
) -> dict:
    """
    Returns Analytics data for a view (profile).

    :param start_date: string, Start date for fetching Analytics data. Requests can specify a start date formatted as YYYY-MM-DD, or as a relative date (e.g., today, yesterday, or 7daysAgo). The default value is 7daysAgo. (required)
    :param end_date: string, End date for fetching Analytics data. Request can should specify an end date formatted as YYYY-MM-DD, or as a relative date (e.g., today, yesterday, or 7daysAgo). The default value is yesterday. (required)
    :param metrics: string, A comma-separated list of Analytics metrics. E.g., 'ga:sessions,ga:pageviews'. At least one metric must be specified. (required)
    :param filters: string, A comma-separated list of dimension or metric filters to be applied to Analytics data.
    :param sort: string, A comma-separated list of dimensions or metrics that determine the sort order for Analytics data.
    :param include_empty_rows: boolean, The response will include empty rows if this parameter is set to true, the default is true
    :param segment: string, An Analytics segment to be applied to data.
    :param output: string, The selected format for the response. Default format is JSON.
        - Allowed values
            - dataTable - Returns the response in Google Charts Data Table format. This is useful in creating visualization using Google Charts.
            - json - Returns the response in standard JSON format.
    :param max_results: integer, The maximum number of entries to include in this feed.
    :param start_index: integer, An index of the first entity to retrieve. Use this parameter as a pagination mechanism along with the max-results parameter.
    :param sampling_level: string, The desired sampling level.
        - Allowed values
                - DEFAULT - Returns response with a sample size that balances speed and accuracy.
                - FASTER - Returns a fast response with a smaller sample size.
                - HIGHER_PRECISION - Returns a more accurate response using a large sample size, but this may result in the response being slower.
    :param dimensions: string, A comma-separated list of Analytics dimensions. E.g., 'ga:browser,ga:city'.

    Learn more at: http://googleapis.github.io/google-api-python-client/docs/dyn/analytics_v3.data.ga.html
    """
    service = get_service()
    profile_id: str = f"ga:{settings.GOOGLE_API_PROFILE_ID}"
    return (
        service.data()
        .ga()
        .get(
            ids=profile_id,
            start_date=start_date,
            end_date=end_date,
            metrics=metrics,
            filters=filters,
            sort=sort,
            include_empty_rows=include_empty_rows,
            segment=segment,
            output=output,
            max_results=max_results,
            start_index=start_index,
            samplingLevel=sampling_level,
            dimensions=dimensions
        )
        .execute()
    )


def get_results_mcf(
    start_date: str,
    end_date: str,
    metrics: str,
    filters: str = None,
    sort: str = None,
    max_results: int = None,
    start_index: int = None,
    sampling_level: str = None,
    dimensions: str = None,
) -> dict:
    """
    Returns Analytics Multi-Channel Funnels data for a view (profile).

    :param start_date: string, Start date for fetching Analytics data. Requests can specify a start date formatted as YYYY-MM-DD, or as a relative date (e.g., today, yesterday, or 7daysAgo). The default value is 7daysAgo. (required)
    :param end_date: string, End date for fetching Analytics data. Requests can specify a start date formatted as YYYY-MM-DD, or as a relative date (e.g., today, yesterday, or 7daysAgo). The default value is 7daysAgo. (required)
    :param metrics: string, A comma-separated list of Multi-Channel Funnels metrics. E.g., 'mcf:totalConversions,mcf:totalConversionValue'. At least one metric must be specified. (required)
    :param filters: string, A comma-separated list of dimension or metric filters to be applied to the Analytics data.
    :param sort: string, A comma-separated list of dimensions or metrics that determine the sort order for the Analytics data.
    :param max_results: integer, The maximum number of entries to include in this feed.
    :param start_index: integer, An index of the first entity to retrieve. Use this parameter as a pagination mechanism along with the max-results parameter.
    :param sampling_level: string, The desired sampling level.
        - Allowed values
                - DEFAULT - Returns response with a sample size that balances speed and accuracy.
                - FASTER - Returns a fast response with a smaller sample size.
                - HIGHER_PRECISION - Returns a more accurate response using a large sample size, but this may result in the response being slower.
    :param dimensions: string, A comma-separated list of Multi-Channel Funnels dimensions. E.g., 'mcf:source,mcf:medium'.

    Learn more at: http://googleapis.github.io/google-api-python-client/docs/dyn/analytics_v3.data.mcf.html
    """
    service = get_service()
    profile_id: str = f"ga:{settings.GOOGLE_API_PROFILE_ID}"
    return (
        service.data()
        .mcf()
        .get(
            ids=profile_id,
            start_date=start_date,
            end_date=end_date,
            metrics=metrics,
            filters=filters,
            sort=sort,
            max_results=max_results,
            start_index=start_index,
            samplingLevel=sampling_level,
            dimensions=dimensions,
        )
        .execute()
    )


def get_results_realtime(
    metrics: str,
    filters: str = None,
    sort: str = None,
    max_results: int = None,
    dimensions: str = None,
) -> dict:
    """
    Returns real time data for a view (profile).

    :param metrics: string, A comma-separated list of real time metrics. E.g., 'rt:activeUsers'. At least one metric must be specified. (required)
    :param filters: string, A comma-separated list of dimension or metric filters to be applied to real time data.
    :param sort: string, A comma-separated list of dimensions or metrics that determine the sort order for real time data.
    :param max_results: integer, The maximum number of entries to include in this feed.
    :param dimensions: string, A comma-separated list of real time dimensions. E.g., 'rt:medium,rt:city'.

    Learn more at: http://googleapis.github.io/google-api-python-client/docs/dyn/analytics_v3.data.realtime.html
    """
    service = get_service()
    profile_id: str = f"ga:{settings.GOOGLE_API_PROFILE_ID}"
    return (
        service.data()
        .realtime()
        .get(
            ids=profile_id,
            metrics=metrics,
            filters=filters,
            sort=sort,
            max_results=max_results,
            dimensions=dimensions,
        )
        .execute()
    )

# todo: add to doc and readme
# https://developers.google.com/analytics/devguides/reporting/core/v3/quickstart/service-py?hl=pt-br
# https://github.com/googleapis/oauth2client
# Install google lib: sudo pip install --upgrade google-api-python-client
# Install oauth2client lib: pip install --upgrade oauth2client
# Create a service account:
# https://console.developers.google.com/iam-admin/serviceaccounts?hl=pt-br
# Create a project in google google_analytics
# Enable api in google google_analytics:
# https://console.developers.google.com/apis/api/analytics.googleapis.com/overview
# In google_analytics admin give permision to service account created
