from account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from holiday.models import EmployeeWorkingDay
from .tasks import create_employee_salary_view_task, create_employee_working_day_task
from django.db import transaction

@receiver(post_save, sender=User)
def create_employee_salary_view(sender, instance, created, **kwargs):
    if created:
        instance_id = instance.id
        transaction.on_commit(lambda: create_employee_salary_view_task.delay(instance_id))
        # create_employee_salary_view_task.delay(instance_id)

@receiver(post_save, sender=User)
def create_employee_working_day(sender, instance, created, **kwargs):
    if created:
        instance_id = instance.id
        transaction.on_commit(lambda: create_employee_working_day_task.delay(instance_id))
        # create_employee_working_day_task.delay(instance_id)