from django.db import models
from services import PAY_METHOD_CHOICES, CASH
from django.contrib.auth import get_user_model

User = get_user_model()

class Service(models.Model):
    create_date = models.DateField(null=True, blank=True)
    appointment_date = models.DateField(null=True, blank=True)
    service_date = models.DateField(null=True, blank=True)
    customer = models.ForeignKey("account.Customer", on_delete=models.CASCADE, null=True, blank=True, related_name="services")
    contract = models.ForeignKey("contract.Contract", on_delete=models.CASCADE, null=True, blank=True, related_name="services")
    product = models.ManyToManyField("product.Product", related_name="services")
    product_quantity = models.CharField(max_length=500, null=True, blank=True)
    pay_method = models.CharField(max_length=50, choices=PAY_METHOD_CHOICES, default=CASH)
    price = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    total_paid_amount = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    remaining_payment = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    loan_term = models.IntegerField(default=0, null=True)
    discount = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    is_done = models.BooleanField(default=False)
    initial_payment = models.DecimalField(default=0, max_digits=20, decimal_places=0, blank=True)
    note = models.TextField(default="", null=True, blank=True)
    service_creditor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="service_creaditors")
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="service_opeartors")
    is_auto = models.BooleanField(default=False)
    delay = models.BooleanField(default=False)
    delay_date = models.DateField(null=True, blank=True)
    start_date_of_payment = models.DateField(null=True, blank=True)
    guarantee = models.PositiveBigIntegerField(null=True, blank=True)
    is_finished = models.BooleanField(default=False)

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
    create_date = models.DateField(auto_now_add=True)
    service_amount = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    service_paid_amount = models.DecimalField(default=0, max_digits=20, decimal_places=0)
    is_done = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
    service_paid_date = models.DateTimeField(null=True, blank=True)
    note = models.TextField(default="", null=True, blank=True)
    remaining_debt = models.DecimalField(default=0, null=True, blank=True, max_digits=20, decimal_places=0)

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
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name="service_product_for_contracts")
    service_period = models.IntegerField(default=1)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="service_for_contracts")
    
    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_serviceproductforcontract", "Müqaviləyə periodik servis üçün təyin olunmuş məhsullara baxa bilər"),
            ("add_serviceproductforcontract", "Müqaviləyə periodik servis üçün məhsullar əlavə edə bilər"),
            ("change_serviceproductforcontract", "Müqaviləyə periodik servis üçün təyin olunmuş məhsulların məlumatlarını yeniləyə bilər"),
            ("delete_serviceproductforcontract", "Müqaviləyə periodik servis üçün təyin olunmuş məhsulları silə bilər")
        )
