from celery import shared_task

from .tracking import tracking


@shared_task()
def run_tracking_check():
    tracking()
    return "completed"
