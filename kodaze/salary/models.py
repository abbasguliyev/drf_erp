import django
from django.db import models
import datetime
from django.contrib.auth import get_user_model
from . import SALARY_RANGE_STYLE_CHOICES


USER = get_user_model()

class AbstractPrim(models.Model):
    KREDIT = 'KREDİT'
    NAGD = 'NƏĞD'
    ODENIS_USLUBU_CHOICES = [
        (KREDIT, "KREDİT"),
        (NAGD, "NƏĞD"),
    ]

    prim_status = models.ForeignKey('account.EmployeeStatus', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, null=True, blank=True)
    sales_amount = models.FloatField(default=0, null=True, blank=True)
    payment_style =  models.CharField(
        max_length=20,
        choices=ODENIS_USLUBU_CHOICES,
        default=NAGD
    )
    position = models.ForeignKey('company.Position', on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

class AbstractSalaryMethod(models.Model):
    employee = models.ForeignKey(USER, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, blank=True)
    note = models.TextField(default="", blank=True)
    date = models.DateField(default=django.utils.timezone.now, blank=True)

    class Meta:
        abstract = True


class OfficeLeaderPrim(AbstractPrim):
    payment_style = None
    prim_for_office = models.FloatField(default=0, blank=True)
    fix_prim = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_officeleaderprim", "Mövcud ofis leader primlərə baxa bilər"),
            ("add_officeleaderprim", "Ofis Leader prim əlavə edə bilər"),
            ("change_officeleaderprim", "Ofis Leader prim məlumatlarını yeniləyə bilər"),
            ("delete_officeleaderprim", "Ofis Leader prim silə bilər")
        )


class GroupLeaderPrimNew(AbstractPrim):
    payment_style = None
    cash = models.FloatField(default=0, blank=True)
    installment_4_12 = models.FloatField(default=0, blank=True)
    installment_13_18 = models.FloatField(default=0, blank=True)
    installment_19_24 = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_groupleaderprimnew", "Mövcud group leader primlərə baxa bilər"),
            ("add_groupleaderprimnew", "GroupLeader prim əlavə edə bilər"),
            ("change_groupleaderprimnew", "GroupLeader prim məlumatlarını yeniləyə bilər"),
            ("delete_groupleaderprimnew", "GroupLeader prim silə bilər")
        )


class Manager1PrimNew(AbstractPrim):
    payment_style = None
    cash = models.FloatField(default=0, blank=True)
    installment_4_12 = models.FloatField(default=0, blank=True)
    installment_13_18 = models.FloatField(default=0, blank=True)
    installment_19_24 = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_manager1primnew", "Mövcud manager1 primlərə baxa bilər"),
            ("add_manager1primnew", "Manager1 prim əlavə edə bilər"),
            ("change_manager1primnew", "Manager1 prim məlumatlarını yeniləyə bilər"),
            ("delete_manager1primnew", "Manager1 prim silə bilər")
        )

class Manager2Prim(AbstractPrim):
    payment_style = None
    sale0 = models.FloatField(default=0, blank=True)
    sale1_8 = models.FloatField(default=0, blank=True)
    sale9_14 = models.FloatField(default=0, blank=True)
    sale15p = models.FloatField(default=0, blank=True)
    sale20p = models.FloatField(default=0, blank=True)
    prim_for_team = models.FloatField(default=0, blank=True)
    prim_for_office = models.FloatField(default=0, blank=True)
    fix_prim = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_manager2prim", "Mövcud manager2 primlərə baxa bilər"),
            ("add_manager2prim", "Manager2 prim əlavə edə bilər"),
            ("change_manager2prim", "Manager2 prim məlumatlarını yeniləyə bilər"),
            ("delete_manager2prim", "Manager2 prim silə bilər")
        )


class CreditorPrim(models.Model):
    prim_percent = models.PositiveBigIntegerField(default=0, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_creditorprim", "Mövcud kreditor primlərə baxa bilər"),
            ("add_creditorprim", "Kreditor prim əlavə edə bilər"),
            ("change_creditorprim", "Kreditor prim məlumatlarını yeniləyə bilər"),
            ("delete_creditorprim", "Kreditor prim silə bilər")
        )

# -----------------------------------------------------------------------------------------------------------------------------

class MonthRange(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    start_month = models.PositiveIntegerField(default=0)
    end_month = models.PositiveIntegerField(default=0)

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
    end_count = models.PositiveIntegerField(default=0)

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
    for_office = models.FloatField(default=0, blank=True)
    cash = models.FloatField(default=0, blank=True)
    for_team = models.FloatField(default=0, blank=True)
    installment = models.ManyToManyField(CommissionInstallment, related_name="installments")
    for_sale_range = models.ManyToManyField(CommissionSaleRange, related_name="for_sale_ranges")
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

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_salaryview", "Mövcud maaş cədvəllərinə baxa bilər"),
            ("add_salaryview", "Maaş cədvəli əlavə edə bilər"),
            ("change_salaryview", "Maaş cədvəlinin məlumatlarını yeniləyə bilər"),
            ("delete_salaryview", "Maaş cədvəlini silə bilər")
        )