import django_filters

from cashbox.models import (
    HoldingCashbox,
    CompanyCashbox,
    OfficeCashbox,
    CashFlow
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

            'initial_balance': ['exact', 'gte', 'lte'],
            'subsequent_balance': ['exact', 'gte', 'lte'],
            'description': ['exact', 'icontains'],

            'operation_style': ['exact', 'icontains'],
            
            # 'date': ['exact', 'gte', 'lte'],
        }