import requests
from datetime import datetime
from celery.task import task
from django.conf import settings
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from .models import Flow, DailyFlowRuns, Group, DailyGroupCount, DailyChannelCount, Channel
from .rapidpro import get_flow


@task(name="sync-daily-flow-run")
def sync_daily_flow_run():
    rapidpro_flow_data = get_flow()
    # next = rapidpro_flow_data.get("next")
    results = rapidpro_flow_data.get("results")

    rows_added = 0
    for result in results:
        uuid = result.get("uuid")
        try:
            flow = Flow.objects.get(uuid=uuid)
            total_runs_database = flow.runs.all().aggregate(
                total_completed=Coalesce(Sum("completed"), 0),
                total_interrupted=Coalesce(Sum("interrupted"), 0),
                total_expired=Coalesce(Sum("expired"), 0)
            )

            new_total_runs = result.get("runs")

            daily_completed = new_total_runs.get("completed", 0) - total_runs_database.get("total_completed", 0)
            daily_interrupted = new_total_runs.get("interrupted", 0) - total_runs_database.get("total_interrupted", 0)
            daily_expired = new_total_runs.get("expired", 0) - total_runs_database.get("total_expired", 0)

            new_daily_run = DailyFlowRuns.objects.create(
                flow=flow,
                active=new_total_runs.get("active", 0),
                completed=daily_completed,
                interrupted=daily_interrupted,
                expired=daily_expired,
                day=timezone.now()
            )
            rows_added += 1

        except Flow.DoesNotExist:
            pass

    return f"Rows added: {rows_added}"


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
            daily_group_count = DailyGroupCount.objects.create(group=group, count=count, day=timezone.now())

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
            channel_daily = DailyChannelCount(channel=channel, count=values, day=datetime_values)
