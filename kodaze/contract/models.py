from django.db import models
import django
from core.image_validator import file_size
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

from . import (
    ARTIQ_ODEME_STATUS_CHOICES,
    BORCU_BAGLA_STATUS_CHOICES,
    CONTRACT_STATUS_CHOICES,
    CONTINUING,
    CASH,
    GECIKDIRME_STATUS_CHOICES,
    INITIAL_PAYMENT_DEBT_STATUS_CHOICES,
    INITIAL_PAYMENT_STATUS_CHOICES,
    INSTALLMENT,
    MODIFIED_PRODUCT_STATUS_CHOICES,
    NATAMAM_STATUS_CHOICES,
    NEW_GRAPH_CHOICES,
    NONE,
    ODEME_STATUS_CHOICES,
    ODENIS_USLUBU_CHOICES,
    ODENMEYEN,
    PAYMENT_STYLE_CHOICES,
    SERTLI_ODEME_STATUSU,
    SIFIR_STATUS_CHOICES
)

from django.db.models import F


USER = get_user_model()


# Create your models here.
class Contract(models.Model):
    group_leader = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="group_leader", null=True,
                                     blank=True)
    manager1 = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="manager1", null=True,
                                 blank=True)
    manager2 = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="manager2", null=True,
                                 blank=True)
    customer = models.ForeignKey('account.Customer', on_delete=models.CASCADE, related_name="contracts", null=True,
                                blank=True)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="contracts", null=True,
                               blank=True)
    product_quantity = models.PositiveIntegerField(default=1, blank=True)
    total_amount = models.FloatField(default=0, blank=True)
    electronic_signature = models.ImageField(upload_to="media/contract/%Y/%m/%d/", null=True, blank=True,
                                      validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    contract_date = models.DateField(null=True, blank=True)
    contract_created_date = models.DateField(auto_now_add=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name="contracts", null=True,
                                blank=True)
    office = models.ForeignKey('company.Office', on_delete=models.CASCADE, related_name="contracts", null=True, blank=True)
    remaining_debt = models.FloatField(default=0, blank=True)
    is_remove = models.BooleanField(default=False)
    loan_term = models.IntegerField(default=0, blank=True)
    initial_payment = models.FloatField(blank=True, null=True)
    initial_payment_debt = models.FloatField(blank=True, null=True)
    initial_payment_date = models.DateField(blank=True, null=True)
    initial_payment_debt_date = models.DateField(blank=True, null=True)
    pdf = models.FileField(upload_to="media/media/contract_doc/%Y/%m/%d/", blank=True, null=True,
                           validators=[file_size, FileExtensionValidator(['pdf'])])
    pdf2 = models.FileField(upload_to="media/media/contract_doc/%Y/%m/%d/", blank=True, null=True,
                                 validators=[file_size, FileExtensionValidator(['pdf'])])

    cancelled_date = models.DateField(null=True, blank=True)
    debt_closing_date = models.DateField(null=True, blank=True)

    compensation_income = models.FloatField(default=0, null=True, blank=True)
    compensation_expense = models.FloatField(default=0, null=True, blank=True)

    debt_finished = models.BooleanField(default=False, blank=True)
    note = models.TextField(null=True, blank=True)


    payment_style = models.CharField(
        max_length=20,
        choices=PAYMENT_STYLE_CHOICES,
        default=CASH
    )

    new_graphic_amount = models.FloatField(default=0, blank=True)
    new_graphic_status = models.CharField(
        max_length=50,
        choices=NEW_GRAPH_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    modified_product_status = models.CharField(
        max_length=50,
        choices=MODIFIED_PRODUCT_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    contract_status = models.CharField(
        max_length=20,
        choices=CONTRACT_STATUS_CHOICES,
        default=CONTINUING
    )

    initial_payment_status = models.CharField(
        max_length=20,
        choices=INITIAL_PAYMENT_STATUS_CHOICES,
        default=NONE
    )

    initial_payment_debt_status = models.CharField(
        max_length=20,
        choices=INITIAL_PAYMENT_DEBT_STATUS_CHOICES,
        default=NONE
    )

    def save(self, *args, **kwargs) -> None:
        self.total_amount = self.product_quantity * self.product.price
        super(Contract, self).save(*args, **kwargs)
    

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
        ordering = ("pk",)
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
    price = models.FloatField(default=0, blank=True)
    payment_status = models.CharField(
        max_length=30,
        choices=ODEME_STATUS_CHOICES,
        default=ODENMEYEN
    )

    conditional_payment_status = models.CharField(
        max_length=50,
        choices=SERTLI_ODEME_STATUSU,
        default=None,
        null=True,
        blank=True
    )

    close_the_debt_status = models.CharField(
        max_length=30,
        choices=BORCU_BAGLA_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    delay_status = models.CharField(
        max_length=30,
        choices=GECIKDIRME_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    missed_month_substatus = models.CharField(
        max_length=20,
        choices=SIFIR_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    incomplete_month_substatus = models.CharField(
        max_length=20,
        choices=NATAMAM_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    overpayment_substatus = models.CharField(
        max_length=20,
        choices=ARTIQ_ODEME_STATUS_CHOICES,
        default=None,
        null=True,
        blank=True
    )

    last_month = models.BooleanField(default=False)
    note = models.TextField(default="", blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_installment", "Mövcud ödəmələrə baxa bilər"),
            ("add_installment", "Ödəmə əlavə edə bilər"),
            ("change_installment", "Ödəmə məlumatlarını yeniləyə bilər"),
            ("delete_installment", "Ödəmə silə bilər")
        )


class ContractChange(models.Model):
    old_contract = models.ForeignKey(Contract, related_name="changed_contracts", on_delete=models.CASCADE)
    payment_style = models.CharField(max_length=100, choices=ODENIS_USLUBU_CHOICES, default=INSTALLMENT)
    loan_term = models.IntegerField(default=0, blank=True)
    product = models.ForeignKey("product.Product", related_name="changed_contracts", on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_contractchange", "Mövcud dəyişimlərə baxa bilər"),
            ("add_contractchange", "Dəyişim əlavə edə bilər"),
            ("change_contractchange", "Dəyişim məlumatlarını yeniləyə bilər"),
            ("delete_contractchange", "Dəyişim silə bilər")
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

