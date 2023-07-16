from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.http import HttpResponse, request
from django.urls import reverse

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mailganer.settings")

app = Celery("mailganer")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'app.task.add',
#         'schedule': 30.0,
#         'args': (16, 6)
#     },
# }
# app.conf.timezone = 'Europe/Moscow'

app.conf.beat_schedule = {
    "add-every-30-seconds": {
        "task": "app.task.send_mails_task",
        "schedule": 10.0,
        "args": (),
    },
}
app.conf.timezone = "Europe/Moscow"
