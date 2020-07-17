from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthbuddy_backend.settings')

app = Celery('healthbuddy_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'sync-daily-flow-run': {
        'task': 'sync-daily-flow-run',
        'schedule': crontab(minute=50, hour=18)
    },
}
app.conf.timezone = "UTC"

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
