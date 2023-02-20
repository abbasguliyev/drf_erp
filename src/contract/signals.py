import time
from .models import Contract
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import create_installment_task, demo_sale_count_task

from contract.api.services.installment_create_service import installment_create

from . import (
    INSTALLMENT
)

from django.db import transaction

@receiver(post_save, sender=Contract)
def create_installment(sender, instance, created, **kwargs):
    if created:
        if(instance.payment_style == INSTALLMENT):
            instance_id = instance.id
            transaction.on_commit(lambda: create_installment_task.delay(instance_id))

@receiver(post_save, sender=Contract)
def demo_sale_count(sender, instance, created, **kwargs):
    if created:
        instance_id = instance.id
        transaction.on_commit(lambda: demo_sale_count_task.delay(instance_id))
