import django
from django.db import models
from django.core.validators import FileExtensionValidator
from account.models import User
from core.image_validator import file_size
from django.contrib.auth import get_user_model
from django.db.models import F
from . import (
    TRANSFER,
    EMELIYYAT_NOVU_CHOICES,
)
User = get_user_model()


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    office = models.ForeignKey(
        'company.Office', on_delete=models.CASCADE, null=True, related_name="warehouses")
    company = models.ForeignKey(
        'company.Company', on_delete=models.CASCADE, null=True, related_name="warehouses")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_warehouse", "Mövcud anbarlara baxa bilər"),
            ("add_warehouse", "Anbar əlavə edə bilər"),
            ("change_warehouse", "Anbar məlumatlarını yeniləyə bilər"),
            ("delete_warehouse", "Anbar silə bilər")
        )

class WarehouseRequest(models.Model):
    employee_who_sent_the_request = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="warehouse_requests")
    product_and_quantity = models.CharField(max_length=250, null=True, blank=True)
    note = models.TextField()
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="warehouse_note")
    is_done = models.BooleanField(default=False)
    request_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_warehouserequest", "Mövcud anbar sorğularına baxa bilər"),
            ("add_warehouserequest", "Anbar sorğu əlavə edə bilər"),
            ("change_warehouserequest", "Anbar sorğu məlumatlarını yeniləyə bilər"),
            ("delete_warehouserequest", "Anbar sorğu silə bilər")
        )


class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse, null=True, on_delete=models.CASCADE, related_name="stocks")
    product = models.ForeignKey(
        "product.Product", null=True, on_delete=models.CASCADE, related_name="stocks")
    quantity = models.IntegerField(default=0)
    date = models.DateField(auto_now=True, blank=True)
    note = models.TextField(default="", null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        constraints = [
            models.UniqueConstraint(
                fields=["warehouse", "product"], name="unique name for your constraint"
            )
        ]
        default_permissions = []
        permissions = (
            ("view_stok", "Mövcud stoklara baxa bilər"),
            ("add_stok", "Stock əlavə edə bilər"),
            ("change_stok", "Stock məlumatlarını yeniləyə bilər"),
            ("delete_stok", "Stock silə bilər")
        )

    def increase_stock(self, quantity: int):
        """Return given quantity of product to a stock."""
        self.quantity = F("quantity") + quantity
        self.save(update_fields=["quantity"])

    def decrease_stock(self, quantity: int):
        self.quantity = F("quantity") - quantity
        self.save(update_fields=["quantity"])


class Operation(models.Model):
    shipping_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, null=True, related_name="shipping_warehouse")
    receiving_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, null=True, related_name="receiving_warehouse")

    product_and_quantity = models.CharField(max_length=500, null=True, blank=True)

    note = models.TextField(default="", null=True, blank=True)
    operation_date = models.DateField(
        auto_now_add=True, null=True, blank=True)

    operation_type = models.CharField(
        max_length=50, choices=EMELIYYAT_NOVU_CHOICES, default=TRANSFER)

    quantity = models.IntegerField(default=0, blank=True, null=True)
    executor = models.ForeignKey(
        User, related_name="operation", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_operation", "Mövcud əməliyyatlara baxa bilər"),
            ("add_operation", "Əməliyyat əlavə edə bilər"),
            ("change_operation", "Əməliyyat məlumatlarını yeniləyə bilər"),
            ("delete_operation", "Əməliyyat silə bilər")
        )