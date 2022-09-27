import django_filters

from warehouse.models import (
    Operation, 
    Warehouse, 
    WarehouseRequest, 
    Stock
)

class StockFilter(django_filters.FilterSet):
    class Meta:
        model = Stock
        fields = {
            'product__id': ['exact'],
            'product__product_name': ['exact', 'icontains'],
            'product__price': ['exact', 'gte', 'lte'],

            'warehouse__company__name': ['exact', 'icontains'],
            'warehouse__office__name': ['exact', 'icontains'],
            'warehouse__name': ['exact', 'icontains'],
            'product__is_hediyye': ['exact'],
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

            # 'operation_date': ['exact', 'gte', 'lte'],
        }

class WarehouseFilter(django_filters.FilterSet):
    class Meta:
        model = Warehouse
        fields = {
            'name': ['exact', 'icontains'],
            'is_active': ['exact'],
            'office__name': ['exact', 'icontains'],
            'office__company__name': ['exact', 'icontains'],
        }

class WarehouseRequestFilter(django_filters.FilterSet):
    class Meta:
        model = WarehouseRequest
        fields = {
            'note': ['exact', 'icontains'],
            'warehouse__name': ['exact', 'icontains'],
            'warehouse__office__name': ['exact', 'icontains'],
        }