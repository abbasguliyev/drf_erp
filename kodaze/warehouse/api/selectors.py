from django.db.models.query import QuerySet

from warehouse.models import (
    HoldingWarehouse,
    Warehouse,
    Stock,
    ChangeUnuselessOperation
)

def holding_warehouse_list(*, filters=None) -> QuerySet[HoldingWarehouse]:
    filters = filters or {}
    qs = HoldingWarehouse.objects.select_related('product').all()
    return qs

def warehouse_list(*, filters=None) -> QuerySet[Warehouse]:
    filters = filters or {}
    qs = Warehouse.objects.select_related('company', 'office').all()
    return qs

def stock_list(*, filters=None) -> QuerySet[Stock]:
    filters = filters or {}
    qs = Stock.objects.select_related('warehouse', 'product').all()
    return qs

def change_unuseless_operation_list(*, filters=None) -> QuerySet[ChangeUnuselessOperation]:
    filters = filters or {}
    qs = ChangeUnuselessOperation.objects.all()
    return qs