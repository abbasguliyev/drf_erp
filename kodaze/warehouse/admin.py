from django.contrib import admin
from .models import Warehouse, Stock, WarehouseRequest, Operation

# Register your models here.
admin.site.register(Warehouse)
admin.site.register(WarehouseRequest)
admin.site.register(Operation)
admin.site.register(Stock)