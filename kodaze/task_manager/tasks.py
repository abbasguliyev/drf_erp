import datetime
from celery import shared_task
from . models import TaskManager


@shared_task(name='manage_task_manager')
def manage_task_manager():
    indi = datetime.datetime.today()
    tasks = TaskManager.objects.select_related(
        'position', 'employee').filter(status="İcra edilir")
    for task in tasks:
        if (task.type=="tapşırıq"):
            d1 = datetime.datetime(task.end_date.year, task.end_date.month,
                                task.end_date.day, task.end_date.hour, task.end_date.minute, task.end_date.second)
            d2 = datetime.datetime(indi.year, indi.month,
                                indi.day, indi.hour, indi.minute, indi.second)
            if d1 >= d2:
                task.status = "Gecikir"
                task.save()
