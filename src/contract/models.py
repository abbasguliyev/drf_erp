from django.db import models
import django
from core.image_validator import file_size
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

from . import (
    CONTRACT_STATUS_CHOICES,
    CONTINUING,
    CASH,
    INITIAL_PAYMENT_DEBT_STATUS_CHOICES,
    INITIAL_PAYMENT_STATUS_CHOICES,
    MODIFIED_PRODUCT_STATUS_CHOICES,
    NONE,
    PAID_STATUS_CHOICES,
    ODENMEYEN,
    PAYMENT_STYLE_CHOICES,
    CLOSE_THE_DEBT_STATUS_CHOICES,
    GECIKDIRME_STATUS_CHOICES
)

from django.db.models import F


USER = get_user_model()


# Create your models here.
class Contract(models.Model):
    group_leader = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="group_leader", null=True, blank=True)
    manager1 = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="manager1", null=True, blank=True)
    manager2 = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="manager2", null=True, blank=True)
    customer = models.ForeignKey('account.Customer', on_delete=models.CASCADE, related_name="contracts", null=True, blank=True)
    region = models.ForeignKey("account.Region", on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="contracts", null=True, blank=True)
    product_quantity = models.PositiveIntegerField(default=1, blank=True)
    total_amount = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    electronic_signature = models.ImageField(upload_to="media/contract/%Y/%m/%d/", null=True, blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    contract_date = models.DateField(null=True, blank=True)
    contract_created_date = models.DateField(auto_now_add=True)
    installment_start_date = models.DateField(null=True, blank=True)
    is_holding_contract = models.BooleanField(default=False)
    is_conditional_contract = models.BooleanField(default=False)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name="contracts", null=True, blank=True)
    office = models.ForeignKey('company.Office', on_delete=models.CASCADE, related_name="contracts", null=True, blank=True)
    remaining_debt = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    loan_term = models.IntegerField(default=0, blank=True)
    discount = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    
    initial_payment = models.DecimalField(default=0, null=True, blank=True, max_digits=20, decimal_places=0)
    paid_initial_payment = models.DecimalField(default=0, null=True, blank=True, max_digits=20, decimal_places=0)
    initial_payment_debt = models.DecimalField(default=0, null=True, blank=True, max_digits=20, decimal_places=0)
    paid_initial_payment_debt = models.DecimalField(default=0, null=True, blank=True, max_digits=20, decimal_places=0)
    initial_payment_date = models.DateField(blank=True, null=True)
    initial_payment_paid_date = models.DateTimeField(blank=True, null=True)
    initial_payment_debt_date = models.DateField(blank=True, null=True)
    initial_payment_debt_paid_date = models.DateTimeField(blank=True, null=True)
    
    pdf = models.FileField(upload_to="media/media/contract_doc/%Y/%m/%d/", blank=True, null=True, validators=[file_size, FileExtensionValidator(['pdf'])])

    compensation_income = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    compensation_expense = models.DecimalField(default=0, max_digits=20, decimal_places=0)

    debt_finished = models.BooleanField(default=False, blank=True)
    debt_closing_date = models.DateField(null=True, blank=True)
    
    note = models.TextField(null=True, blank=True)
    conditional_contract_note = models.TextField(null=True, blank=True)
    default_installment_amount = models.DecimalField(default=0, null=True, blank=True, max_digits=20, decimal_places=0)

    payment_style = models.CharField(
        max_length=20,
        choices=PAYMENT_STYLE_CHOICES,
        default=CASH
    )

    intervention_product_status = models.CharField(
        max_length=50,
        choices=MODIFIED_PRODUCT_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    intervention_date = models.DateField(null=True, blank=True)
    contract_change_date = models.DateField(null=True, blank=True)
    contract_removed_date = models.DateField(null=True, blank=True)
    cancelled_contract = models.BooleanField(default=False)
    changed_new_contract = models.BooleanField(default=False)
    contract_status = models.CharField(
        max_length=20,
        choices=CONTRACT_STATUS_CHOICES,
        default=CONTINUING
    )

    initial_payment_status = models.CharField(
        max_length=20,
        choices=INITIAL_PAYMENT_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    initial_payment_debt_status = models.CharField(
        max_length=20,
        choices=INITIAL_PAYMENT_DEBT_STATUS_CHOICES,
        default=NONE,
        null=True,
        blank=True
    )
    old_contract = models.ForeignKey("self", on_delete=models.SET_NULL, related_name="changed_contracts", null=True, blank=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_contract", "Mövcud müqavilələrə baxa bilər"),
            ("add_contract", "Müqavilə əlavə edə bilər"),
            ("change_contract", "Müqavilə məlumatlarını yeniləyə bilər"),
            ("delete_contract", "Müqavilə silə bilər")
        )


class ContractCreditor(models.Model):
    creditor = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="creditor_contracts")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="creditors")

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_contractcreditor", "Mövcud kreditorlara baxa bilər"),
            ("add_contractcreditor", "Müqaviləyə kreditor əlavə edə bilər"),
            ("change_contractcreditor", "Müqavilənin kreditor məlumatlarını yeniləyə bilər"),
            ("delete_contractcreditor", "Müqavilənin kreditorunu silə bilər")
        )


class ContractGift(models.Model):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, null=True, blank=True, related_name="gifts")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="gifts")
    quantity = models.PositiveBigIntegerField(default=1)
    gift_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_contractgift", "Mövcud müqavilə hədiyyələrə baxa bilər"),
            ("add_contractgift", "Müqaviləy' hədiyyə əlavə edə bilər"),
            ("change_contractgift", "Müqavilənin hədiyyə məlumatlarını yeniləyə bilər"),
            ("delete_contractgift", "Müqavilənin hədiyyəsini silə bilər")
        )


class Installment(models.Model):
    month_no = models.PositiveIntegerField(default=1)
    contract = models.ForeignKey(Contract, blank=True, null=True, related_name='installments',
                                 on_delete=models.CASCADE)
    date = models.DateField(default=False, blank=True, null=True)
    paid_date = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    paid_price = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    is_paid = models.BooleanField(default=False)
    payment_status = models.CharField(
        max_length=30,
        choices=PAID_STATUS_CHOICES,
        default=ODENMEYEN
    )

    delay_status = models.CharField(
        max_length=30,
        choices=GECIKDIRME_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )
    close_the_debt_status = models.CharField(
        max_length=50,
        choices=CLOSE_THE_DEBT_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    last_month = models.BooleanField(default=False)
    note = models.TextField(default="", blank=True, null=True)
    remaining_debt = models.DecimalField(default=0, null=True, blank=True, max_digits=20, decimal_places=0)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_installment", "Mövcud ödəmələrə baxa bilər"),
            ("add_installment", "Ödəmə əlavə edə bilər"),
            ("change_installment", "Ödəmə məlumatlarını yeniləyə bilər"),
            ("delete_installment", "Ödəmə silə bilər")
        )

class DemoSales(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="demos")
    count = models.IntegerField(default=0)
    created_date = models.DateField(default=django.utils.timezone.now, blank=True)
    sale_count = models.IntegerField(default=0)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_demosales", "Mövcud demo satışlara baxa bilər"),
            ("add_demosales", "Demo satış əlavə edə bilər"),
            ("change_demosales", "Demo satış məlumatlarını yeniləyə bilər"),
            ("delete_demosales", "Demo satış silə bilər")
        )

