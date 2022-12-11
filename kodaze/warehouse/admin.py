from django.contrib import admin
from .models import Warehouse, HoldingWarehouse, Stock, WarehouseRequest, Operation, ChangeUnuselessOperation

# Register your models here.
admin.site.register(Warehouse)
admin.site.register(WarehouseRequest)
admin.site.register(Operation)
admin.site.register(Stock)

@admin.register(HoldingWarehouse)
class HoldingWarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "useful_product_count", "unuseful_product_count")
    list_display_links = ("id", "product")



@admin.register(ChangeUnuselessOperation)
class ChangeUnuselessOperationAdmin(admin.ModelAdmin):
    list_display = ("id", "products_and_quantity")
    list_display_links = ("id", "products_and_quantity")

