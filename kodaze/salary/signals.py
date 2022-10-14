from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import create_prim_task
from contract.models import Contract
from django.db import transaction

@receiver(post_save, sender=Contract)
def create_prim(sender, instance, created, **kwargs):
    if created:
        instance_id = instance.id
        transaction.on_commit(lambda: create_prim_task.delay(instance_id))