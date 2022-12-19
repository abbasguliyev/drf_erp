import django
from django.db import models

from services import PAY_METHOD_CHOICES, CASH


class Service(models.Model):
    create_date = models.DateField(auto_now_add=True)
    appointment_date = models.DateField(null=True, blank=True)
    service_date = models.DateField(null=True, blank=True)
    customer = models.ForeignKey("account.Customer", on_delete=models.CASCADE, null=True, blank=True, related_name="services")
    contract = models.ForeignKey("contract.Contract", on_delete=models.CASCADE, null=True, blank=True, related_name="services")
    product = models.ManyToManyField("product.Product", related_name="services")
    pay_method = models.CharField(max_length=50, choices=PAY_METHOD_CHOICES, default=CASH)
    price = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    loan_term = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    is_done = models.BooleanField(default=False)
    initial_payment = models.FloatField(default=0, blank=True)
    total_amount_to_be_paid = models.FloatField(default=0)
    confirmation = models.BooleanField(default=False)
    note = models.TextField(default="", null=True, blank=True)
    is_auto = models.BooleanField(default=False)


    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_service", "Mövcud servislərə baxa bilər"),
            ("add_service", "Servis əlavə edə bilər"),
            ("change_service", "Servis məlumatlarını yeniləyə bilər"),
            ("delete_service", "Servis silə bilər")
        )


class ServicePayment(models.Model):
    service = models.ForeignKey(Service, related_name="service_payment", null=True, on_delete=models.CASCADE)
    total_amount_to_be_paid = models.FloatField(default=0, blank=True)
    amount_to_be_paid = models.FloatField(default=0, blank=True)
    is_done = models.BooleanField(default=False)
    payment_date = models.DateField(default=django.utils.timezone.now, blank=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_servicepayment", "Mövcud service ödəmələrinə baxa bilər"),
            ("add_servicepayment", "Service ödəmə əlavə edə bilər"),
            ("change_servicepayment", "Service ödəmə məlumatlarını yeniləyə bilər"),
            ("delete_servicepayment", "Service ödəmə silə bilər")
        )


class ServiceProductForContract(models.Model):
    service_period = models.IntegerField(default=1)
    product = models.ManyToManyField(
        "product.Product", related_name="service_for_contracts")

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_serviceproductforcontract",
             "Müqaviləyə periodik servis üçün təyin olunmuş məhsullara baxa bilər"),
            ("add_serviceproductforcontract",
             "Müqaviləyə periodik servis üçün məhsullar əlavə edə bilər"),
            ("change_serviceproductforcontract",
             "Müqaviləyə periodik servis üçün təyin olunmuş məhsulların məlumatlarını yeniləyə bilər"),
            ("delete_serviceproductforcontract",
             "Müqaviləyə periodik servis üçün təyin olunmuş məhsulları silə bilər")
        )
