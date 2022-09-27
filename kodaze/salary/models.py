import django
from django.db import models
import datetime
from django.contrib.auth import get_user_model

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

class AdvancePayment(AbstractSalaryMethod):
    half_month_salary = models.PositiveBigIntegerField(default=0, blank=True)
    
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
    installment = models.DateField(default=django.utils.timezone.now, null=True, blank=True)
    
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