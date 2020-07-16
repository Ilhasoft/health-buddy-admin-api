from django.db import models

from .rapidpro import get_flow


class Flow(models.Model):
    uuid = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    def get_flow_data(self):
        flow_data = get_flow(self.uuid)
        return flow_data

    @classmethod
    def get_all_flow_data(cls):
        all_flow_data = get_flow("")
        return all_flow_data


class DailyFlowRuns(models.Model):
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name="runs")
    active = models.PositiveIntegerField(default=0)
    completed = models.PositiveIntegerField(default=0)
    interrupted = models.PositiveIntegerField(default=0)
    expired = models.PositiveIntegerField(default=0)
    day = models.DateTimeField()
