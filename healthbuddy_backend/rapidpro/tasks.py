from celery.task import task
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from .models import Flow, DailyFlowRuns
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
                total_active=Coalesce(Sum("active"), 0),
                total_completed=Coalesce(Sum("completed"), 0),
                total_interrupted=Coalesce(Sum("interrupted"), 0),
                total_expired=Coalesce(Sum("expired"), 0)
            )

            new_total_runs = result.get("runs")

            daily_active = new_total_runs.get("active", 0) - total_runs_database.get("total_active", 0)
            daily_completed = new_total_runs.get("completed", 0) - total_runs_database.get("total_completed", 0)
            daily_interrupted = new_total_runs.get("interrupted", 0) - total_runs_database.get("total_interrupted", 0)
            daily_expired = new_total_runs.get("expired", 0) - total_runs_database.get("total_expired", 0)

            new_daily_run = DailyFlowRuns.objects.create(
                flow=flow,
                active=daily_active,
                completed=daily_completed,
                interrupted=daily_interrupted,
                expired=daily_expired,
                day=timezone.now()
            )
            rows_added += 1

        except Flow.DoesNotExist:
            pass

    return f"Rows added: {rows_added}"
