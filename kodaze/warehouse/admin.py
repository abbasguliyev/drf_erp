from django.contrib import admin
from .models import Warehouse, HoldingWarehouse, Stock, WarehouseRequest, ChangeUnuselessOperation, WarehouseHistory

# Register your models here.
admin.site.register(Warehouse)
admin.site.register(WarehouseRequest)
admin.site.register(WarehouseHistory)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("id", "warehouse", "product", "quantity", "useful_product_count")
    list_display_links = ("id", "warehouse", "product")

@admin.register(HoldingWarehouse)
class HoldingWarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "useful_product_count", "unuseful_product_count")
    list_display_links = ("id", "product")

@admin.register(ChangeUnuselessOperation)
class ChangeUnuselessOperationAdmin(admin.ModelAdmin):
    list_display = ("id", "products_and_quantity")
    list_display_links = ("id", "products_and_quantity")

