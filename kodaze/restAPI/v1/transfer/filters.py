import django_filters

from transfer.models import (
    HoldingdenShirketlereTransfer,
    ShirketdenHoldingeTransfer,
    ShirketdenOfislereTransfer,
    OfisdenShirketeTransfer,
)

class HoldingdenShirketlereTransferFilter(django_filters.FilterSet):
    transfer_tarixi = django_filters.DateFilter(
        field_name='transfer_tarixi', input_formats=["%d-%m-%Y"])
    transfer_tarixi__gte = django_filters.DateFilter(
        field_name='transfer_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    transfer_tarixi__lte = django_filters.DateFilter(
        field_name='transfer_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = HoldingdenShirketlereTransfer
        fields = {
            'transfer_eden__asa': ['exact', 'icontains'],
            'transfer_eden__vezife__vezife_adi': ['exact', 'icontains'],
            'transfer_eden__isci_status__status_adi': ['exact', 'icontains'],

            'holding_kassa__holding__holding_adi': ['exact', 'icontains'],
            'shirket_kassa__shirket__shirket_adi': ['exact', 'icontains'],

            'transfer_meblegi': ['exact', 'gte', 'lte'],
            'transfer_qeydi': ['exact', 'icontains'],
            
            # 'transfer_tarixi': ['exact', 'gte', 'lte'],
        }


class ShirketdenHoldingeTransferFilter(django_filters.FilterSet):
    transfer_tarixi = django_filters.DateFilter(
        field_name='transfer_tarixi', input_formats=["%d-%m-%Y"])
    transfer_tarixi__gte = django_filters.DateFilter(
        field_name='transfer_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    transfer_tarixi__lte = django_filters.DateFilter(
        field_name='transfer_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = ShirketdenHoldingeTransfer
        fields = {
            'transfer_eden__asa': ['exact', 'icontains'],
            'transfer_eden__vezife__vezife_adi': ['exact', 'icontains'],
            'transfer_eden__isci_status__status_adi': ['exact', 'icontains'],

            'holding_kassa__holding__holding_adi': ['exact', 'icontains'],
            'shirket_kassa__shirket__shirket_adi': ['exact', 'icontains'],

            'transfer_meblegi': ['exact', 'gte', 'lte'],
            'transfer_qeydi': ['exact', 'icontains'],
            
            # 'transfer_tarixi': ['exact', 'gte', 'lte'],
        }

class ShirketdenOfislereTransferFilter(django_filters.FilterSet):
    transfer_tarixi = django_filters.DateFilter(
        field_name='transfer_tarixi', input_formats=["%d-%m-%Y"])
    transfer_tarixi__gte = django_filters.DateFilter(
        field_name='transfer_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    transfer_tarixi__lte = django_filters.DateFilter(
        field_name='transfer_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = ShirketdenOfislereTransfer
        fields = {
            'transfer_eden__asa': ['exact', 'icontains'],
            'transfer_eden__vezife__vezife_adi': ['exact', 'icontains'],
            'transfer_eden__isci_status__status_adi': ['exact', 'icontains'],

            'ofis_kassa__ofis__ofis_adi': ['exact', 'icontains'],
            'shirket_kassa__shirket__shirket_adi': ['exact', 'icontains'],

            'transfer_meblegi': ['exact', 'gte', 'lte'],
            'transfer_qeydi': ['exact', 'icontains'],
            
            # 'transfer_tarixi': ['exact', 'gte', 'lte'],
        }

class OfisdenShirketeTransferFilter(django_filters.FilterSet):
    transfer_tarixi = django_filters.DateFilter(
        field_name='transfer_tarixi', input_formats=["%d-%m-%Y"])
    transfer_tarixi__gte = django_filters.DateFilter(
        field_name='transfer_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    transfer_tarixi__lte = django_filters.DateFilter(
        field_name='transfer_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = OfisdenShirketeTransfer
        fields = {
            'transfer_eden__asa': ['exact', 'icontains'],
            'transfer_eden__vezife__vezife_adi': ['exact', 'icontains'],
            'transfer_eden__isci_status__status_adi': ['exact', 'icontains'],

            'ofis_kassa__ofis__ofis_adi': ['exact', 'icontains'],
            'shirket_kassa__shirket__shirket_adi': ['exact', 'icontains'],

            'transfer_meblegi': ['exact', 'gte', 'lte'],
            'transfer_qeydi': ['exact', 'icontains'],
            
            # 'transfer_tarixi': ['exact', 'gte', 'lte'],
        }