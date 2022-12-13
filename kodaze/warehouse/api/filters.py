import django_filters

from warehouse.models import (
    Warehouse, 
    WarehouseRequest, 
    Stock,
    HoldingWarehouse
)

class StockFilter(django_filters.FilterSet):
    class Meta:
        model = Stock
        fields = {
            'product': ['exact'],
            'product__product_name': ['exact', 'icontains'],
            'product__price': ['exact', 'gte', 'lte'],
            'product__barcode': ['exact', 'gte', 'lte'],

            'warehouse__company': ['exact'],
            'warehouse': ['exact'],
            'product__is_gift': ['exact'],
        }

class WarehouseFilter(django_filters.FilterSet):
    class Meta:
        model = Warehouse
        fields = {
            'name': ['exact', 'icontains'],
            'is_active': ['exact'],
            'office': ['exact'],
            'company': ['exact'],
        }

class WarehouseRequestFilter(django_filters.FilterSet):
    class Meta:
        model = WarehouseRequest
        fields = {
            'note': ['exact', 'icontains'],
            'warehouse__name': ['exact', 'icontains'],
            'warehouse__office__name': ['exact', 'icontains'],
        }


class HoldingWarehouseFilter(django_filters.FilterSet):
    class Meta:
        model = HoldingWarehouse
        fields = {
            'product': ['exact'],
            'product__product_name': ['exact', 'icontains'],
            'product__barcode': ['exact', 'icontains'],
            'quantity': ['exact'],
            'useful_product_count': ['exact'],
            'unuseful_product_count': ['exact'],
        }
