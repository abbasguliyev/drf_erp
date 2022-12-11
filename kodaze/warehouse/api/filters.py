import django_filters

from warehouse.models import (
    Operation, 
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

class OperationFilter(django_filters.FilterSet):
    operation_date = django_filters.DateFilter(
        field_name='operation_date', input_formats=["%d-%m-%Y"])
    operation_date__gte = django_filters.DateFilter(
        field_name='operation_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    operation_date__lte = django_filters.DateFilter(
        field_name='operation_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = Operation
        fields = {
            'shipping_warehouse__name': ['exact', 'icontains'],
            'shipping_warehouse__office__name': ['exact', 'icontains'],
            'shipping_warehouse__company__name': ['exact', 'icontains'],

            'receiving_warehouse__name': ['exact', 'icontains'],
            'receiving_warehouse__office__name': ['exact', 'icontains'],
            'receiving_warehouse__company__name': ['exact', 'icontains'],

            'note': ['exact', 'icontains'],
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
