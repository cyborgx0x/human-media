from celery import shared_task
from .tracking import tracking
@shared_task
def run_tracking_check(file_name):
    '''
    nhớ input filename, celery task không nhận các data mà nó không JSON serializing được.
    '''
    '''
    check file tracking
    '''
    tracking(filename=file_name)
    return "completed"

