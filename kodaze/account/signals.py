from account.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from holiday.models import EmployeeWorkingDay
from .tasks import (
    create_employee_salary_view_task, 
    create_employee_working_day_task, 
    create_user_permission_for_position_task
)
from django.db import transaction

from django.core.cache import cache

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

@receiver(post_save, sender=User)
def create_user_permission_for_position(sender, instance, created, **kwargs):
    if created:
        instance_id = instance.id
        transaction.on_commit(lambda: create_user_permission_for_position_task.delay(instance_id))
        # create_user_permission_for_position_task.delay(instance_id)

@receiver(post_delete, sender=User, dispatch_uid='post_deleted')
def object_post_delete_handler(sender, **kwargs):
    cache.delete_many(keys=cache.keys('*.users.*'))


@receiver(post_save, sender=User, dispatch_uid='posts_updated')
def object_post_save_handler(sender, **kwargs):
    cache.delete_many(keys=cache.keys('*.users.*'))

@receiver(post_save, sender=User)
def object_post_save_handler(sender, **kwargs):
    cache.delete_many(keys=cache.keys('*.users.*'))
