from contract.models import Contract
from . models import Service
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import pandas as pd
from django.db import transaction

from .tasks import create_services_task, create_service_payment_task


@receiver(post_save, sender=Contract)
def create_services(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: create_services_task.delay(instance.id))


@receiver(post_save, sender=Service)
def create_service_payment(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: create_service_payment_task.delay(instance.id))