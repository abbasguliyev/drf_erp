import django_filters

from transfer.models import (
    TransferFromHoldingToCompany,
    TransferFromCompanyToHolding,
    TransferFromCompanyToOffices,
    TransferFromOfficeToCompany,
)

class TransferFromHoldingToCompanyFilter(django_filters.FilterSet):
    transfer_date = django_filters.DateFilter(
        field_name='transfer_date', input_formats=["%d-%m-%Y"])
    transfer_date__gte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    transfer_date__lte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = TransferFromHoldingToCompany
        fields = {
            'executor__fullname': ['exact', 'icontains'],
            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'holding_cashbox__holding__name': ['exact', 'icontains'],
            'company_cashbox__company__name': ['exact', 'icontains'],

            'transfer_amount': ['exact', 'gte', 'lte'],
            'transfer_note': ['exact', 'icontains'],
            
            # 'transfer_date': ['exact', 'gte', 'lte'],
        }


class TransferFromCompanyToHoldingFilter(django_filters.FilterSet):
    transfer_date = django_filters.DateFilter(
        field_name='transfer_date', input_formats=["%d-%m-%Y"])
    transfer_date__gte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    transfer_date__lte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = TransferFromCompanyToHolding
        fields = {
            'executor__fullname': ['exact', 'icontains'],
            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'holding_cashbox__holding__name': ['exact', 'icontains'],
            'company_cashbox__company__name': ['exact', 'icontains'],

            'transfer_amount': ['exact', 'gte', 'lte'],
            'transfer_note': ['exact', 'icontains'],
            
            # 'transfer_date': ['exact', 'gte', 'lte'],
        }

class TransferFromCompanyToOfficesFilter(django_filters.FilterSet):
    transfer_date = django_filters.DateFilter(
        field_name='transfer_date', input_formats=["%d-%m-%Y"])
    transfer_date__gte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    transfer_date__lte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = TransferFromCompanyToOffices
        fields = {
            'executor__fullname': ['exact', 'icontains'],
            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'office_cashbox__office__name': ['exact', 'icontains'],
            'company_cashbox__company__name': ['exact', 'icontains'],

            'transfer_amount': ['exact', 'gte', 'lte'],
            'transfer_note': ['exact', 'icontains'],
            
            # 'transfer_date': ['exact', 'gte', 'lte'],
        }

class TransferFromOfficeToCompanyFilter(django_filters.FilterSet):
    transfer_date = django_filters.DateFilter(
        field_name='transfer_date', input_formats=["%d-%m-%Y"])
    transfer_date__gte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    transfer_date__lte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = TransferFromOfficeToCompany
        fields = {
            'executor__fullname': ['exact', 'icontains'],
            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'office_cashbox__office__name': ['exact', 'icontains'],
            'company_cashbox__company__name': ['exact', 'icontains'],

            'transfer_amount': ['exact', 'gte', 'lte'],
            'transfer_note': ['exact', 'icontains'],
            
            # 'transfer_date': ['exact', 'gte', 'lte'],
        }