import datetime
from celery import shared_task
from . models import TaskManager


@shared_task(name='manage_task_manager')
def manage_task_manager():
    now = datetime.datetime.today()
    tasks = TaskManager.objects.select_related(
        'position', 'employee').filter(status="İcra edilir")
    for task in tasks:
        d1 = datetime.date(task.end_date.year, task.end_date.month, task.end_date.day)
        d2 = datetime.date.today()
        if d1 <= d2:
            task.status = "Gecikir"
            task.save()
