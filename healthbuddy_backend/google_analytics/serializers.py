from rest_framework import serializers


class GAGoogleAnalyticsAPISerializer(serializers.Serializer):
    """ids
    start_date
    end_date
    metrics
    filters=None
    sort=None
    include_empty_rows=None
    segment=None
    output=None
    max_results=None
    start_index=None
    samplingLevel=None
    dimensions=None"""
    ...


class MCFGoogleAnalyticsAPISerializer(serializers.Serializer):
    """ids
    start_date
    end_date
    metrics
    filters=None
    sort=None
    max_results=None
    start_index=None
    samplingLevel=None
    dimensions=None"""
    ...


class RealTimeGoogleAnalyticsAPISerializer(serializers.Serializer):
    """ids
    metrics
    filters=None
    sort=None
    max_results=None
    dimensions=None"""
    ...
