import django_filters
from django.db.models import Q

from cashbox.models import (
    HoldingCashbox,
    CompanyCashbox,
    OfficeCashbox,
    CashFlow,
    HoldingCashboxOperation,
    CompanyCashboxOperation,
    CostType
)

class HoldingCashboxFilter(django_filters.FilterSet):
    class Meta:
        model = HoldingCashbox
        fields = {
            'holding__id': ['exact'],
            'holding__name': ['exact', 'icontains'],
            'balance': ['exact', 'gte', 'lte'],
        }

class CompanyCashboxFilter(django_filters.FilterSet):
    class Meta:
        model = CompanyCashbox
        fields = {
            'company__id': ['exact'],
            'company__name': ['exact', 'icontains'],
            'company__is_active': ['exact'],
            'balance': ['exact', 'gte', 'lte'],
        }

class OfficeCashboxFilter(django_filters.FilterSet):
    class Meta:
        model = OfficeCashbox
        fields = {
            'office__id': ['exact'],
            'office__name': ['exact', 'icontains'],
            'office__is_active': ['exact'],
            'office__company__id': ['exact'],
            'office__company__name': ['exact', 'icontains'],

            'balance': ['exact', 'gte', 'lte'],
        }

class CashFlowFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    is_holding = django_filters.BooleanFilter(method="is_holding_filter", label="is_holding")

    def is_holding_filter(self, queryset, name, value):
        qs = None
        if value == True:
            qs = queryset.filter(
                ~Q(holding=None) & Q(office=None) & Q(company=None) 
            )
        elif value == False:
            qs = queryset.filter(
                ~Q(office=None) & ~Q(company=None)
            )
        else:
            qs = queryset
        return qs

    class Meta:
        model = CashFlow
        fields = {
            'executor': ['exact'],
            'executor__fullname': ['exact', 'icontains'],

            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'holding__name': ['exact', 'icontains'],
            'holding': ['exact'],

            'office__name': ['exact', 'icontains'],
            'office': ['exact'],

            'company__name': ['exact', 'icontains'],
            'company': ['exact'],
            'personal': ['exact'],
            'customer': ['exact'],

            'balance': ['exact', 'gte', 'lte'],
            'description': ['exact', 'icontains'],

            'operation_style': ['exact', 'icontains'],
            'cost_type': ['exact'],
        }

class HoldingCashboxOperationFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = HoldingCashboxOperation
        fields = {
            'executor': ['exact'],
            'amount': ['exact',],
            'executor': ['exact',],
        }

class CompanyCashboxOperationFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = CompanyCashboxOperation
        fields = {
            'executor': ['exact'],
            'amount': ['exact',],
            'executor': ['exact',],
            'office': ['exact'],
            'office__id': ['exact'],
            'office__name': ['exact', 'icontains'],
        }

class CostTypeFilter(django_filters.FilterSet):
    class Meta:
        model = CostType
        fields = {
            'name': ['exact', 'icontains']
        }