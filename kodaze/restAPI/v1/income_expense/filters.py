import django_filters

from income_expense.models import (
    HoldingKassaMedaxil,
    HoldingKassaMexaric,
    OfisKassaMedaxil,
    OfisKassaMexaric,
    ShirketKassaMedaxil,
    ShirketKassaMexaric,
)

class HoldingKassaMedaxilFilter(django_filters.FilterSet):
    class Meta:
        model = HoldingKassaMedaxil
        fields = {
            'medaxil_eden__asa': ['exact', 'icontains'],
            'medaxil_eden__vezife__vezife_adi': ['exact', 'icontains'],
            'medaxil_eden__isci_status__status_adi': ['exact', 'icontains'],

            'holding_kassa__holding__holding_adi': ['exact', 'icontains'],
            'mebleg': ['exact', 'gte', 'lte'],
            'qeyd': ['exact', 'icontains'],
            
            'medaxil_tarixi': ['exact', 'gte', 'lte'],

        }

class HoldingKassaMexaricFilter(django_filters.FilterSet):
    class Meta:
        model = HoldingKassaMexaric
        fields = {
            'mexaric_eden__asa': ['exact', 'icontains'],
            'mexaric_eden__vezife__vezife_adi': ['exact', 'icontains'],
            'mexaric_eden__isci_status__status_adi': ['exact', 'icontains'],

            'holding_kassa__holding__holding_adi': ['exact', 'icontains'],
            'mebleg': ['exact', 'gte', 'lte'],
            'qeyd': ['exact', 'icontains'],
            
            'mexaric_tarixi': ['exact', 'gte', 'lte'],
        }

class ShirketKassaMedaxilFilter(django_filters.FilterSet):
    class Meta:
        model = ShirketKassaMedaxil
        fields = {
            'medaxil_eden__asa': ['exact', 'icontains'],
            'medaxil_eden__vezife__vezife_adi': ['exact', 'icontains'],
            'medaxil_eden__isci_status__status_adi': ['exact', 'icontains'],

            'shirket_kassa__shirket__shirket_adi': ['exact', 'icontains'],
            'mebleg': ['exact', 'gte', 'lte'],
            'qeyd': ['exact', 'icontains'],
            
            'medaxil_tarixi': ['exact', 'gte', 'lte'],

        }

class ShirketKassaMexaricFilter(django_filters.FilterSet):
    class Meta:
        model = ShirketKassaMexaric
        fields = {
            'mexaric_eden__asa': ['exact', 'icontains'],
            'mexaric_eden__vezife__vezife_adi': ['exact', 'icontains'],
            'mexaric_eden__isci_status__status_adi': ['exact', 'icontains'],

            'shirket_kassa__shirket__shirket_adi': ['exact', 'icontains'],
            'mebleg': ['exact', 'gte', 'lte'],
            'qeyd': ['exact', 'icontains'],
            
            'mexaric_tarixi': ['exact', 'gte', 'lte'],
        }

class OfisKassaMedaxilFilter(django_filters.FilterSet):
    class Meta:
        model = OfisKassaMedaxil
        fields = {
            'medaxil_eden__asa': ['exact', 'icontains'],
            'medaxil_eden__vezife__vezife_adi': ['exact', 'icontains'],
            'medaxil_eden__isci_status__status_adi': ['exact', 'icontains'],

            'ofis_kassa__ofis__ofis_adi': ['exact', 'icontains'],
            'mebleg': ['exact', 'gte', 'lte'],
            'qeyd': ['exact', 'icontains'],
            
            'medaxil_tarixi': ['exact', 'gte', 'lte'],

        }

class OfisKassaMexaricFilter(django_filters.FilterSet):
    class Meta:
        model = OfisKassaMexaric
        fields = {
            'mexaric_eden__asa': ['exact', 'icontains'],
            'mexaric_eden__vezife__vezife_adi': ['exact', 'icontains'],
            'mexaric_eden__isci_status__status_adi': ['exact', 'icontains'],

            'ofis_kassa__ofis__ofis_adi': ['exact', 'icontains'],
            'mebleg': ['exact', 'gte', 'lte'],
            'qeyd': ['exact', 'icontains'],
            
            'mexaric_tarixi': ['exact', 'gte', 'lte'],
        }
