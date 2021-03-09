from django.db import models

from .rapidpro import get_flow


class Flow(models.Model):
    uuid = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def get_flow_data(self):
        flow_data = get_flow(self.uuid)
        return flow_data

    @classmethod
    def get_all_flow_data(cls):
        all_flow_data = get_flow("")
        return all_flow_data


class DailyFlowRuns(models.Model):
    flow = models.ForeignKey(Flow, on_delete=models.PROTECT, related_name="runs")
    active = models.PositiveIntegerField(default=0)
    completed = models.PositiveIntegerField(default=0)
    interrupted = models.PositiveIntegerField(default=0)
    expired = models.PositiveIntegerField(default=0)
    day = models.DateTimeField()


class Group(models.Model):
    uuid = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)


class DailyGroupCount(models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name="counts")
    count = models.PositiveIntegerField(default=0)
    day = models.DateTimeField()


class Channel(models.Model):
    uuid = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)


class DailyChannelCount(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, related_name="counts")
    count = models.PositiveIntegerField(default=0)
    day = models.DateTimeField()


class Label(models.Model):
    uuid = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.uuid} - {self.name}"


class LabelMessage(models.Model):
    labels = models.ManyToManyField(Label, related_name="messages")
    id_msg_rp = models.IntegerField("Rapidpro message ID", unique=True)
    day = models.DateTimeField()
