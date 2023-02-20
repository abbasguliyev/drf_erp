from django.contrib import admin
from .models import Warehouse, HoldingWarehouse, Stock, WarehouseRequest, ChangeUnuselessOperation, WarehouseHistory

# Register your models here.
admin.site.register(Warehouse)
admin.site.register(WarehouseRequest)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("id", "warehouse", "product", "quantity", "useful_product_count", "changed_product_count")
    list_display_links = ("id", "warehouse", "product")

@admin.register(HoldingWarehouse)
class HoldingWarehouseAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "useful_product_count", "unuseful_product_count")
    list_display_links = ("id", "product")

@admin.register(ChangeUnuselessOperation)
class ChangeUnuselessOperationAdmin(admin.ModelAdmin):
    list_display = ("id", "products_and_quantity")
    list_display_links = ("id", "products_and_quantity")

@admin.register(WarehouseHistory)
class WarehouseHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "operation_style", "company", "sender_warehouse", "receiving_warehouse", "sender_previous_quantity", "sender_subsequent_quantity", "recepient_previous_quantity", "recepient_subsequent_quantity", "product", "customer", "quantity", "executor", "note")
    list_display_links = ("id",)
