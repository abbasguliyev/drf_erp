from company.models import Holding, Office, Company
from cashbox.api.services.cashbox_services import (
    create_holding_cashbox_service,
    create_company_cashbox_service,
    create_office_cashbox_service
)
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Office)
def create_office_cashbox(sender, instance, created, **kwargs):
    if created:
        create_office_cashbox_service(office = instance)

@receiver(post_save, sender=Company)
def create_company_cashbox(sender, instance, created, **kwargs):
    if created:
        create_company_cashbox_service(holding=instance)

@receiver(post_save, sender=Holding)
def create_holding_cashbox(sender, instance, created, **kwargs):
    if created:
        create_holding_cashbox_service(holding=instance)