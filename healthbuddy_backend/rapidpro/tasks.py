import requests
from celery.task import task
from django.conf import settings
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from .models import Flow, DailyFlowRuns, Group, DailyGroupCount
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
