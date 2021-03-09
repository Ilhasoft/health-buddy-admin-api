import requests
from datetime import datetime
from celery.task import task
from django.conf import settings
from django.utils import timezone

from .models import (
    Flow,
    DailyFlowRuns,
    Group,
    DailyGroupCount,
    DailyChannelCount,
    Channel,
    Label,
    LabelMessage,
)


def get_all_results(next_call, headers):
    while next_call:
        response = requests.get(next_call, headers=headers)
        response_json = response.json()
        next_call = response_json.get("next")
        yield response_json.get("results", None)


@task(name="sync-daily-flow-run")
def sync_daily_flow_run():
    next_ = "https://rapidpro.ilhasoft.mobi/api/v2/runs.json"
    headers = {"Authorization": f"Token {settings.TOKEN_ORG_RAPIDPRO}"}

    final_result = {}

    last_item = DailyFlowRuns.objects.last()
    if last_item:
        last_day = last_item.day
        last_day = last_day.strftime("%Y-%m-%d")
        next_ = f"{next_}?after={last_day}"

    while next_:
        response = requests.get(next_, headers=headers)

        json_response = response.json()
        results = json_response.get("results")

        for result in results:
            string_result_date = result.get("created_on")[0:10]

            flow_uuid = result.get("flow", {}).get("uuid")
            if not final_result.get(flow_uuid):
                final_result[flow_uuid] = {}

            if not final_result.get(flow_uuid, {}).get(string_result_date):
                final_result[flow_uuid][string_result_date] = {
                    "active": 0,
                    "completed": 0,
                    "expired": 0,
                    "interrupted": 0
                }

            exit_type = result.get("exit_type")
            if not exit_type:
                final_result[flow_uuid][string_result_date]["active"] += 1
            elif exit_type == "completed":
                final_result[flow_uuid][string_result_date]["completed"] += 1
            elif exit_type == "expired":
                final_result[flow_uuid][string_result_date]["expired"] += 1
            else:
                final_result[flow_uuid][string_result_date]["interrupted"] += 1

        next_ = json_response.get("next")

    for flow_uuid, dates in final_result.items():
        try:
            flow = Flow.objects.get(uuid=flow_uuid)
            for date, values in dates.items():
                datetime_runs = datetime.strptime(date, "%Y-%m-%d")
                DailyFlowRuns.objects.create(
                    flow=flow,
                    day=datetime_runs,
                    active=values.get("active"),
                    completed=values.get("completed"),
                    interrupted=values.get("interrupted"),
                    expired=values.get("expired")
                )
        except Flow.DoesNotExist:
            pass


@task(name="sync-daily-group-count")
def sync_daily_group_count():
    next_ = "https://rapidpro.ilhasoft.mobi/api/v2/groups.json"
    headers = {"Authorization": f"Token {settings.TOKEN_ORG_RAPIDPRO}"}

    rows_added = 0

    while next_:
        response = requests.get(next_, headers=headers)

        json_response = response.json()
        results = json_response.get("results")

        for result in results:
            uuid = result.get("uuid")
            name = result.get("name")
            count = result.get("count")
            group, created = Group.objects.get_or_create(uuid=uuid, name=name)
            DailyGroupCount.objects.create(group=group, count=count, day=timezone.now())

            rows_added += 1

        next_ = json_response.get("next")

    return f"Rows added: {rows_added}"


@task(name="sync-daily-channel-count")
def sync_daily_channel_count():
    next_ = "https://rapidpro.ilhasoft.mobi/api/v2/messages.json"
    headers = {"Authorization": f"Token {settings.TOKEN_ORG_RAPIDPRO}"}

    final_result = {}

    last_item = DailyChannelCount.objects.last()
    if last_item:
        last_day = last_item.day
        last_day = last_day.strftime("%Y-%m-%d")
        next_ = f"{next_}?after={last_day}"

    while next_:
        response = requests.get(next_, headers=headers)

        json_response = response.json()
        results = json_response.get("results")

        for result in results:
            string_result_date = result.get("created_on")[0:10]

            channel_name = result.get("channel", {}).get("name")
            if not final_result.get(channel_name):
                final_result[channel_name] = {
                    "uuid": result.get("channel", {}).get("uuid")
                }

            if not final_result.get(channel_name, {}).get(string_result_date):
                final_result[channel_name][string_result_date] = 0

            final_result[channel_name][string_result_date] += 1

        next_ = json_response.get("next")

    for channel_name, dates_and_uuid in final_result.items():
        channel_uuid = dates_and_uuid.pop("uuid", None)
        channel, created = Channel.objects.get_or_create(uuid=channel_uuid, name=channel_name)

        for dates, values in dates_and_uuid.items():
            datetime_values = datetime.strptime(dates, "%Y-%m-%d")
            DailyChannelCount.objects.create(channel=channel, count=values, day=datetime_values)


@task(name="sync-daily-label-count")
def sync_label_messages():
    headers = {"Authorization": f"Token {settings.TOKEN_ORG_RAPIDPRO}"}

    # Get all rapidpro labels
    labels_url = "https://rapidpro.ilhasoft.mobi/api/v2/labels.json"
    results = get_all_results(labels_url, headers)
    for result in results:
        for label_result in result:
            label, created = Label.objects.get_or_create(
                uuid=label_result.get("uuid"),
                name=label_result.get("name")
            )

            # Get all label messages
            messages_url = f"https://rapidpro.ilhasoft.mobi/api/v2/messages.json?label={label.uuid}"

            last_message = label.messages.last()
            if last_message:
                last_sync_date = last_message.day.strftime("%Y-%m-%d")
                messages_url = f"{messages_url}&after={last_sync_date}"

            results = get_all_results(messages_url, headers)
            for result in results:
                for message in result:
                    label_message, created = LabelMessage.objects.get_or_create(
                        id_msg_rp=message.get("id"),
                        day=message.get("created_on")
                    )
                    label_message.labels.add(label)
