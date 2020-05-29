from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service(key_file_location):
    scopes = ['https://www.googleapis.com/auth/analytics.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file_location, scopes=scopes)
    return build('analytics', 'v3', credentials=credentials)


def get_metric_value(key_file_location, profile_id, metrics='pageviews', start_date='365daysAgo', end_date='today',):
    service = get_service(key_file_location=key_file_location)
    return service.data().ga().get(
            ids='ga:' + profile_id,
            start_date=start_date,
            end_date=end_date,
            metrics='ga:' + metrics).execute().get('totalResults')


def main():
    key_file_location = './sample_key.json'
    profile_id = 'sample'

    print get_metric_value(key_file_location, profile_id)


if __name__ == '__main__':
    main()

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
