from django.db import models
import django
from django.db.models import F
from . import (
    OPERATION_STYLE_CHOICE,
)
from django.contrib.auth import get_user_model

USER = get_user_model()

class Cashbox(models.Model):
    balance = models.DecimalField(
        default=0, max_digits=12, decimal_places=2)

    def increase_balance(self, amount: float):
        self.balance = F('balance') + amount
        self.save(update_fields=["balance"])

    def decrease_balance(self, amount: float):
        self.balance = F('balance') - amount
        self.save(update_fields=["balance"])

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

# -----------------------------------------------------

class CashFlow(models.Model):
    date = models.DateField(default=django.utils.timezone.now, blank=True)
    holding = models.ForeignKey('company.Holding', on_delete=models.CASCADE, null=True, blank=True, related_name="cash_flows")
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, blank=True, related_name="cash_flows")
    office = models.ForeignKey('company.Office', on_delete=models.CASCADE, null=True, blank=True, related_name="cash_flows")
    description = models.TextField(null=True, blank=True)
    initial_balance = models.FloatField(default=0)
    subsequent_balance = models.FloatField(default=0)

    holding_initial_balance = models.FloatField(default=0)
    holding_subsequent_balance = models.FloatField(default=0)
    
    company_initial_balance = models.FloatField(default=0)
    company_subsequent_balance = models.FloatField(default=0)
    
    office_initial_balance = models.FloatField(default=0)
    office_subsequent_balance = models.FloatField(default=0)
    
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