import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "humanmedia.settings")

app = Celery("humanmedia")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
