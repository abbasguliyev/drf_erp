from company.models import Holding, Office, Company
from .models import HoldingCashbox, OfficeCashbox, CompanyCashbox
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Office)
def create_office_cashbox(sender, instance, created, **kwargs):
    if created:
        office_cashbox = OfficeCashbox.objects.select_related(
            "office").filter(office=instance)
        if len(office_cashbox) == 0:
            office = instance
            balance = 0
            office_cashbox = OfficeCashbox.objects.create(
                office=office, balance=balance).save()


@receiver(post_save, sender=Company)
def create_company_cashbox(sender, instance, created, **kwargs):
    if created:
        company_cashbox = CompanyCashbox.objects.select_related(
            "company").filter(company=instance)
        if len(company_cashbox) == 0:
            company = instance
            balance = 0
            company_cashbox = CompanyCashbox.objects.create(
                company=company, balance=balance).save()


@receiver(post_save, sender=Holding)
def create_holding_cashbox(sender, instance, created, **kwargs):
    if created:
        holding_cashbox = HoldingCashbox.objects.select_related(
            "holding").filter(holding=instance)
        if len(holding_cashbox) == 0:
            holding = instance
            balance = 0
            holding_cashbox = HoldingCashbox.objects.create(
                holding=holding, balance=balance).save()
