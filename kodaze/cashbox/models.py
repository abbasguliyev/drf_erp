from django.db import models
import django
from django.db.models import F
from . import (
    OPERATION_STYLE_CHOICE,
    INCOME
)
from django.contrib.auth import get_user_model

USER = get_user_model()

class Cashbox(models.Model):
    title = models.CharField(max_length=150)
    balance = models.FloatField(default=0)
    note = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        abstract = True

class AbstractCashboxOperation(models.Model):
    amount = models.FloatField(default=0)
    note = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    operation = models.CharField(
        max_length = 150,
        choices = OPERATION_STYLE_CHOICE,
        default = INCOME,
    )

    class Meta:
        abstract = True

class OfficeCashbox(Cashbox):
    office = models.ForeignKey("company.Office", on_delete=models.CASCADE, related_name="cashbox")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_officecashbox", "Mövcud ofis kassalara baxa bilər"),
            ("add_officecashbox", "Ofis kassa əlavə edə bilər"),
            ("change_officecashbox", "Ofis kassa məlumatlarını yeniləyə bilər"),
            ("delete_officecashbox", "Ofis kassa silə bilər")
        )


class CompanyCashbox(Cashbox):
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE, related_name="cashbox")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_companycashbox", "Mövcud şirkət kassalara baxa bilər"),
            ("add_companycashbox", "Şirkət kassa əlavə edə bilər"),
            ("change_companycashbox", "Şirkət kassa məlumatlarını yeniləyə bilər"),
            ("delete_companycashbox", "Şirkət kassa silə bilər")
        )


class HoldingCashbox(Cashbox):
    holding = models.ForeignKey("company.Holding", on_delete=models.CASCADE, related_name="cashbox")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_holdingcashbox", "Mövcud holdinq kassalara baxa bilər"),
            ("add_holdingcashbox", "Holdinq kassa əlavə edə bilər"),
            ("change_holdingcashbox", "Holdinq kassa məlumatlarını yeniləyə bilər"),
            ("delete_holdingcashbox", "Holdinq kassa silə bilər")
        )


class CashFlow(models.Model):
    date = models.DateField(default=django.utils.timezone.now, blank=True)
    holding = models.ForeignKey('company.Holding', on_delete=models.CASCADE, null=True, blank=True, related_name="cash_flows")
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, blank=True, related_name="cash_flows")
    office = models.ForeignKey('company.Office', on_delete=models.CASCADE, null=True, blank=True, related_name="cash_flows")
    customer = models.ForeignKey('account.Customer', on_delete=models.CASCADE, null=True, blank=True, related_name="cash_flows")
    personal = models.ForeignKey(USER, on_delete=models.CASCADE, null=True, blank=True, related_name="cash_flow_personals")
    description = models.TextField(null=True, blank=True)
    balance = models.FloatField(default=0)
    executor = models.ForeignKey(USER, related_name="cash_flows", on_delete=models.CASCADE, null=True, blank=True)
    operation_style = models.CharField(max_length=100, choices=OPERATION_STYLE_CHOICE, default=None, null=True, blank=True)
    quantity = models.FloatField(default=0)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_cashflow", "Mövcud pul axınlarına baxa bilər"),
            ("add_cashflow", "Pul axını əlavə edə bilər"),
            ("change_cashflow", "Pul axını məlumatlarını yeniləyə bilər"),
            ("delete_cashflow", "Pul axını məlumatlarını silə bilər")
        )

class HoldingCashboxOperation(AbstractCashboxOperation):
    executor = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="holding_cashbox_operations")
    personal = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="holding_cashbox_operations_personals")
    
    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_holdingcashboxoperation", "Mövcud holdinq kassa əməliyyatlarına baxa bilər"),
            ("add_holdingcashboxoperation", "Holdinq kassa əməliyyatı əlavə edə bilər"),
            ("change_holdingcashboxoperation", "Holdinq kassa əməliyyatı məlumatlarını yeniləyə bilər"),
            ("delete_holdingcashboxoperation", "Holdinq kassa əməliyyatı məlumatlarını silə bilər")
        )

class CompanyCashboxOperation(AbstractCashboxOperation):
    executor = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="company_cashbox_operations")
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name="company_cashbox_operations")
    office = models.ForeignKey('company.Office', on_delete=models.CASCADE, null=True, blank=True, related_name="company_cashbox_operations")
    personal = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="company_cashbox_operations_personals")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_companycashboxoperation", "Mövcud şirkət kassa əməliyyatlarına baxa bilər"),
            ("add_companycashboxoperation", "Şirkət kassa əməliyyatı əlavə edə bilər"),
            ("change_companycashboxoperation", "Şirkət kassa əməliyyatı məlumatlarını yeniləyə bilər"),
            ("delete_companycashboxoperation", "Şirkət kassa əməliyyatı məlumatlarını silə bilər")
        )
