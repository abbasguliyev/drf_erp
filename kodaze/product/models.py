from django.db import models
from django.db.models import (
    F
)
from django.core.validators import FileExtensionValidator
from core.image_validator import file_size


class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_unitofmeasure", "Mövcud ölçü vahidlərinə baxa bilər"),
            ("add_unitofmeasure", "Ölçü vahidi əlavə edə bilər"),
            ("change_unitofmeasure", "Ölçü vahidi məlumatlarını yeniləyə bilər"),
            ("delete_unitofmeasure", "Ölçü vahidini silə bilər")
        )


class Category(models.Model):
    category_name = models.CharField(max_length=200)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_category", "Mövcud kateqoriyalara baxa bilər"),
            ("add_category", "Kateqoriya əlavə edə bilər"),
            ("change_category", "Kateqoriya məlumatlarını yeniləyə bilər"),
            ("delete_category", "Kateqoriya silə bilər")
        )


class Product(models.Model):
    product_name = models.CharField(max_length=300)
    barcode = models.PositiveIntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="products")
    unit_of_measure = models.ForeignKey(UnitOfMeasure, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_price = models.FloatField(default=0, null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    guarantee = models.PositiveIntegerField(default=0)
    is_gift = models.BooleanField(default=False)
    weight = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    product_image = models.ImageField(upload_to="media/product/%Y/%m/%d/", null=True,
                                      blank=True, validators=[file_size, FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_product", "Mövcud məhsullara baxa bilər"),
            ("add_product", "Məhsul əlavə edə bilər"),
            ("change_product", "Məhsul məlumatlarını yeniləyə bilər"),
            ("delete_product", "Məhsul silə bilər")
        )