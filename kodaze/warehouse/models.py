from django.db import models
from account.models import User
from django.contrib.auth import get_user_model

from . import (
    STATUS_CHOICES,
    WAITING,
    OPERATION_STYLE_CHOICES
)

User = get_user_model()

class HoldingWarehouse(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name="holding_warehouse")
    quantity = models.PositiveIntegerField(default=0)
    useful_product_count = models.PositiveIntegerField(default=0)
    unuseful_product_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_holdingwarehouse", "Holding anbarına baxa bilər"),
        )

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    office = models.ForeignKey(
        'company.Office', on_delete=models.CASCADE, null=True, related_name="warehouses")
    company = models.ForeignKey(
        'company.Company', on_delete=models.CASCADE, null=True, related_name="warehouses")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("pk",)
        constraints = [
            models.UniqueConstraint(
                fields=["name", "office"], name="unique name for your warehouse constraint"
            )
        ]
        default_permissions = []
        permissions = (
            ("view_warehouse", "Mövcud anbarlara baxa bilər"),
            ("add_warehouse", "Anbar əlavə edə bilər"),
            ("change_warehouse", "Anbar məlumatlarını yeniləyə bilər"),
            ("delete_warehouse", "Anbar silə bilər")
        )

class WarehouseRequest(models.Model):
    employee_who_sent_the_request = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="warehouse_requests")
    product_and_quantity = models.CharField(max_length=800, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="warehouse_note")
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default=WAITING
    )
    request_date = models.DateField(auto_now_add=True)
    execution_date = models.DateField(null=True, blank=True)

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
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="stocks")
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="stocks")
    quantity = models.PositiveIntegerField(default=0)
    useful_product_count = models.PositiveIntegerField(default=0)
    changed_product_count = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    note = models.TextField(default="", null=True, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_stock", "Mövcud stoklara baxa bilər"),
            ("add_stock", "Stock əlavə edə bilər"),
            ("change_stock", "Stock məlumatlarını yeniləyə bilər"),
            ("delete_stock", "Stock silə bilər")
        )

class ChangeUnuselessOperation(models.Model):
    products_and_quantity = models.CharField(max_length=800)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_changeunuselessoperation", "Mövcud utilizasiyalara baxa bilər"),
            ("add_changeunuselessoperation", "Utilizasiya edə bilər"),
        )

class WarehouseHistory(models.Model):
    date = models.DateField(auto_now_add=True)
    company = models.ForeignKey('company.Company', on_delete=models.SET_NULL, null=True, blank=True, related_name="warehouse_histories")
    sender_warehouse = models.CharField(max_length=250, null=True, blank=True)
    receiving_warehouse = models.CharField(max_length=250, null=True, blank=True)
    sender_previous_quantity = models.PositiveIntegerField(default=0)
    sender_subsequent_quantity = models.PositiveIntegerField(default=0)
    recepient_previous_quantity = models.PositiveIntegerField(default=0)
    recepient_subsequent_quantity = models.PositiveIntegerField(default=0)
    customer = models.ForeignKey('account.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name="warehouse_histories")
    product = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.CharField(max_length=200, null=True, blank=True)
    operation_style = models.CharField(
        max_length=150,
        choices=OPERATION_STYLE_CHOICES,
        blank=True,
        null=True
    )
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="warehouse_histories")
    note = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_warehousehistory", "Mövcud utilizasiyalara baxa bilər"),
        )
