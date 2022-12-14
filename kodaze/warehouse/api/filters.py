import django_filters

from warehouse.models import (
    Warehouse, 
    WarehouseRequest, 
    Stock,
    HoldingWarehouse,
    WarehouseHistory
)

from account.api.selectors import customer_list

from django.db.models import Q

class StockFilter(django_filters.FilterSet):
    class Meta:
        model = Stock
        fields = {
            'product': ['exact'],
            'product__product_name': ['exact', 'icontains'],
            'product__price': ['exact', 'gte', 'lte'],
            'product__barcode': ['exact', 'gte', 'lte'],

            'warehouse__company': ['exact'],
            'warehouse__office': ['exact'],
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

class WarehouseHistoryFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    phone_number = django_filters.CharFilter(method="phone_number_filter", label="phone_number")

    class Meta:
        model = WarehouseHistory
        fields = {
            'customer': ['exact'],
            'customer__fullname': ['exact', 'icontains'],
            'company': ['exact'],
            'sender_warehouse': ['exact'],
            'receiving_warehouse': ['exact'],
            'operation_style': ['exact'],
            'executor': ['exact'],
        }
    
    def phone_number_filter(self, queryset, name, value):
        qs = None
        for term in value.split():
            qs = self.queryset.filter(
                Q(customer__phone_number_1__icontains=term) | Q(customer__phone_number_2__icontains=term) | Q(customer__phone_number_3__icontains=term) | Q(customer__phone_number_4__icontains=term))
        return qs