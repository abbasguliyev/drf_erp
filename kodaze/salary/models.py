import django
from django.db import models
import datetime
from django.contrib.auth import get_user_model
from . import SALARY_RANGE_STYLE_CHOICES

USER = get_user_model()


class AbstractSalaryMethod(models.Model):
    employee = models.ForeignKey(USER, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, blank=True)
    note = models.TextField(default="", null=True, blank=True)
    date = models.DateField(default=django.utils.timezone.now, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        abstract = True


# -----------------------------------------------------------------------------------------------------------------------------

class MonthRange(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    start_month = models.PositiveIntegerField(default=0)
    end_month = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_monthrange", "Mövcud ay aralıqlarına baxa bilər"),
            ("add_monthrange", "Ay aralığı əlavə edə bilər"),
            ("change_monthrange", "Ay aralığı məlumatlarını yeniləyə bilər"),
            ("delete_monthrange", "Ay aralığı silə bilər")
        )


class SaleRange(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    start_count = models.PositiveIntegerField(default=0)
    end_count = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_salerange", "Mövcud satış aralığı baxa bilər"),
            ("add_salerange", "Satış Aralığı əlavə edə bilər"),
            ("change_salerange", "Satış Aralığı məlumatlarını yeniləyə bilər"),
            ("delete_salerange", "Satış Aralığı silə bilər")
        )


class CommissionInstallment(models.Model):
    month_range = models.ForeignKey(MonthRange, on_delete=models.CASCADE, related_name="month_ranges")
    amount = models.FloatField(default=0)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_commissioninstallment", "Mövcud komissiya kreditlərinə baxa bilər"),
            ("add_commissioninstallment", "Komissya kredit əlavə edə bilər"),
            ("change_commissioninstallment", "Komissya kredit məlumatlarını yeniləyə bilər"),
            ("delete_commissioninstallment", "Komissya kredit silə bilər")
        )


class CommissionSaleRange(models.Model):
    sale_range = models.ForeignKey(SaleRange, on_delete=models.CASCADE, related_name="sale_ranges")
    amount = models.FloatField(default=0)
    sale_type = models.CharField(max_length=50, choices=SALARY_RANGE_STYLE_CHOICES, default="fix")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_commissionsalerange", "Mövcud komissiya satış aralığı baxa bilər"),
            ("add_commissionsalerange", "Komissya satış aralığı əlavə edə bilər"),
            ("change_commissionsalerange", "Komissya satış aralığı məlumatlarını yeniləyə bilər"),
            ("delete_commissionsalerange", "Komissya satış aralığı silə bilər")
        )


class Commission(models.Model):
    commission_name = models.CharField(max_length=200)
    for_office = models.FloatField(default=0, null=True, blank=True)
    cash = models.FloatField(default=0, null=True, blank=True)
    for_team = models.FloatField(default=0, null=True, blank=True)
    installment = models.ManyToManyField(CommissionInstallment, related_name="commissions")
    for_sale_range = models.ManyToManyField(CommissionSaleRange, related_name="commissions")
    creditor_per_cent = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_commission", "Mövcud komissiyalara baxa bilər"),
            ("add_commission", "Komissiya əlavə edə bilər"),
            ("change_commission", "Komissiya məlumatlarını yeniləyə bilər"),
            ("delete_commission", "Komissiya silə bilər")
        )


# -----------------------------------------------------------------------------------------------------------------------------

class AdvancePayment(AbstractSalaryMethod):
    amount = models.FloatField(default=0, null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_advancepayment", "Mövcud avanslara baxa bilər"),
            ("add_advancepayment", "Avans əlavə edə bilər"),
            ("change_advancepayment", "Avans məlumatlarını yeniləyə bilər"),
            ("delete_advancepayment", "Avans silə bilər")
        )


class PaySalary(AbstractSalaryMethod):
    salary_date = models.DateField(default=django.utils.timezone.now, null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_paysalary", "Mövcud maaş ödəmələrinə baxa bilər"),
            ("add_paysalary", "Maaş ödəmə əlavə edə bilər"),
            ("change_paysalary", "Maaş ödəmə məlumatlarını yeniləyə bilər"),
            ("delete_paysalary", "Maaş ödəmə silə bilər")
        )


class SalaryDeduction(AbstractSalaryMethod):
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_salarydeduction", "Mövcud kəsintilərə baxa bilər"),
            ("add_salarydeduction", "Kəsinti əlavə edə bilər"),
            ("change_salarydeduction", "Kəsinti məlumatlarını yeniləyə bilər"),
            ("delete_salarydeduction", "Kəsinti silə bilər")
        )


class SalaryPunishment(AbstractSalaryMethod):
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_punishment", "Mövcud cərimələrə baxa bilər"),
            ("add_punishment", "Cərimə əlavə edə bilər"),
            ("change_punishment", "Cərimə məlumatlarını yeniləyə bilər"),
            ("delete_punishment", "Cərimə silə bilər")
        )


class Bonus(AbstractSalaryMethod):
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_bonus", "Mövcud bonuslara baxa bilər"),
            ("add_bonus", "Bonus əlavə edə bilər"),
            ("change_bonus", "Bonus məlumatlarını yeniləyə bilər"),
            ("delete_bonus", "Bonus silə bilər")
        )


class SalaryView(AbstractSalaryMethod):
    employee = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="employee_salary_views")
    sale_quantity = models.PositiveBigIntegerField(default=0, blank=True)
    sales_amount = models.FloatField(default=0, blank=True)
    final_salary = models.FloatField(default=0, blank=True)
    date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    pay_date = models.DateField(null=True, blank=True)
    commission_amount = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_salaryview", "Mövcud maaş cədvəllərinə baxa bilər"),
            ("add_salaryview", "Maaş cədvəli əlavə edə bilər"),
            ("change_salaryview", "Maaş cədvəlinin məlumatlarını yeniləyə bilər"),
            ("delete_salaryview", "Maaş cədvəlini silə bilər")
        )


class GivenCommissionAfterSignContract(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="given_commissions")
    contract = models.ForeignKey("contract.Contract", on_delete=models.CASCADE, related_name="given_commissions")
    amount = models.FloatField(default=0)

class SalaryViewExport(models.Model):
    file_data = models.FileField(upload_to="media/salary/%Y/%m/%d/")
    export_date =models.DateField(auto_now_add=True)