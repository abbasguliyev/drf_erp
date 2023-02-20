from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import create_commission_task
from salary.api.utils import give_commission_after_contract
from contract.models import Contract
from contract import CANCELLED


@receiver(post_save, sender=Contract)
def create_commission(sender, instance, created, **kwargs):
    if created:
        if instance.contract_status != CANCELLED:
            instance_id = instance.id
            transaction.on_commit(lambda: create_commission_task.delay(instance_id))