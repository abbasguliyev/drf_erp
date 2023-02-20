import django_filters

from transfer.models import (
    HoldingTransfer,
    CompanyTransfer,
    OfficeTransfer,
)

class HoldingTransferFilter(django_filters.FilterSet):
    transfer_date = django_filters.DateFilter(
        field_name='transfer_date', input_formats=["%d-%m-%Y"])
    transfer_date__gte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    transfer_date__lte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = HoldingTransfer
        fields = {
            'executor__fullname': ['exact', 'icontains'],
            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'sending_company__name': ['exact', 'icontains'],
            'receiving_company__name': ['exact', 'icontains'],

            'sending_company': ['exact'],
            'receiving_company': ['exact'],

            'recipient_subsequent_balance': ['exact'],
            'sender_subsequent_balance': ['exact'],

            'transfer_amount': ['exact', 'gte', 'lte'],
            'transfer_note': ['exact', 'icontains'],
        }

class CompanyTransferFilter(django_filters.FilterSet):
    transfer_date = django_filters.DateFilter(
        field_name='transfer_date', input_formats=["%d-%m-%Y"])
    transfer_date__gte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    transfer_date__lte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = CompanyTransfer
        fields = {
            'executor__fullname': ['exact', 'icontains'],
            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'company': ['exact'],
            'company__name': ['exact', 'icontains'],

            'sending_office__name': ['exact', 'icontains'],
            'receiving_office__name': ['exact', 'icontains'],

            'sending_office': ['exact'],
            'receiving_office': ['exact'],

            'recipient_subsequent_balance': ['exact'],
            'sender_subsequent_balance': ['exact'],

            'transfer_amount': ['exact', 'gte', 'lte'],
            'transfer_note': ['exact', 'icontains'],
        }

class OfficeTransferFilter(django_filters.FilterSet):
    transfer_date = django_filters.DateFilter(
        field_name='transfer_date', input_formats=["%d-%m-%Y"])
    transfer_date__gte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    transfer_date__lte = django_filters.DateFilter(
        field_name='transfer_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = OfficeTransfer
        fields = {
            'executor__fullname': ['exact', 'icontains'],
            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'company': ['exact'],
            'company__name': ['exact', 'icontains'],
            'sending_office__name': ['exact', 'icontains'],
            'receiving_office__name': ['exact', 'icontains'],

            'sending_office': ['exact'],
            'receiving_office': ['exact'],

            'recipient_subsequent_balance': ['exact'],
            'sender_subsequent_balance': ['exact'],

            'transfer_amount': ['exact', 'gte', 'lte'],
            'transfer_note': ['exact', 'icontains'],
        }