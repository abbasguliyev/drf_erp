import django_filters

from warehouse.models import (
    Emeliyyat, 
    Anbar, 
    AnbarQeydler, 
    Stok
)

class StokFilter(django_filters.FilterSet):
    class Meta:
        model = Stok
        fields = {
            'mehsul__id': ['exact'],
            'mehsul__mehsulun_adi': ['exact', 'icontains'],
            'mehsul__qiymet': ['exact', 'gte', 'lte'],

            'anbar__shirket__shirket_adi': ['exact', 'icontains'],
            'anbar__ofis__ofis_adi': ['exact', 'icontains'],
            'anbar__ad': ['exact', 'icontains'],
            'mehsul__is_hediyye': ['exact'],
            'mehsul__kartric_novu': ['exact'],
        }

class EmeliyyatFilter(django_filters.FilterSet):
    emeliyyat_tarixi = django_filters.DateFilter(
        field_name='emeliyyat_tarixi', input_formats=["%d-%m-%Y"])
    emeliyyat_tarixi__gte = django_filters.DateFilter(
        field_name='emeliyyat_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    emeliyyat_tarixi__lte = django_filters.DateFilter(
        field_name='emeliyyat_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = Emeliyyat
        fields = {
            'gonderen__ad': ['exact', 'icontains'],
            'gonderen__ofis__ofis_adi': ['exact', 'icontains'],
            'gonderen__shirket__shirket_adi': ['exact', 'icontains'],

            'qebul_eden__ad': ['exact', 'icontains'],
            'qebul_eden__ofis__ofis_adi': ['exact', 'icontains'],
            'qebul_eden__shirket__shirket_adi': ['exact', 'icontains'],

            'qeyd': ['exact', 'icontains'],

            # 'emeliyyat_tarixi': ['exact', 'gte', 'lte'],
        }

class AnbarFilter(django_filters.FilterSet):
    class Meta:
        model = Anbar
        fields = {
            'ad': ['exact', 'icontains'],
            'is_active': ['exact'],
            'ofis__ofis_adi': ['exact', 'icontains'],
            'ofis__shirket__shirket_adi': ['exact', 'icontains'],
        }

class AnbarQeydlerFilter(django_filters.FilterSet):
    class Meta:
        model = AnbarQeydler
        fields = {
            'qeyd': ['exact', 'icontains'],
            'anbar__ad': ['exact', 'icontains'],
            'anbar__ofis__ofis_adi': ['exact', 'icontains'],
        }