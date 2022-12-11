from django.contrib import admin
from .models import Product, Category, UnitOfMeasure

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "purchase_price", "price")
    list_display_links = ("id", "product_name")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")
    list_display_links = ("id", "category_name")

@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")