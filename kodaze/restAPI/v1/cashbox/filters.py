import django_filters

from cashbox.models import (
    HoldingKassa,
    ShirketKassa,
    OfisKassa,
    PulAxini
)
class HoldingKassaFilter(django_filters.FilterSet):
    class Meta:
        model = HoldingKassa
        fields = {
            'holding__id': ['exact'],
            'holding__holding_adi': ['exact', 'icontains'],
            'balans': ['exact', 'gte', 'lte'],
        }

class ShirketKassaFilter(django_filters.FilterSet):
    class Meta:
        model = ShirketKassa
        fields = {
            'shirket__id': ['exact'],
            'shirket__shirket_adi': ['exact', 'icontains'],
            'shirket__is_active': ['exact'],
            'balans': ['exact', 'gte', 'lte'],
        }

class OfisKassaFilter(django_filters.FilterSet):
    class Meta:
        model = OfisKassa
        fields = {
            'ofis__id': ['exact'],
            'ofis__ofis_adi': ['exact', 'icontains'],
            'ofis__is_active': ['exact'],
            'ofis__shirket__id': ['exact'],
            'ofis__shirket__shirket_adi': ['exact', 'icontains'],

            'balans': ['exact', 'gte', 'lte'],
        }

class PulAxiniFilter(django_filters.FilterSet):
    tarix = django_filters.DateFilter(field_name='tarix', input_formats=["%d-%m-%Y"])
    tarix__gte = django_filters.DateFilter(field_name='tarix', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    tarix__lte = django_filters.DateFilter(field_name='tarix', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = PulAxini
        fields = {
            'emeliyyat_eden': ['exact'],
            'emeliyyat_eden__asa': ['exact', 'icontains'],

            'emeliyyat_eden__vezife__vezife_adi': ['exact', 'icontains'],
            'emeliyyat_eden__isci_status__status_adi': ['exact', 'icontains'],

            'holding__holding_adi': ['exact', 'icontains'],
            'holding': ['exact'],

            'ofis__ofis_adi': ['exact', 'icontains'],
            'ofis': ['exact'],

            'shirket__shirket_adi': ['exact', 'icontains'],
            'shirket': ['exact'],

            'ilkin_balans': ['exact', 'gte', 'lte'],
            'sonraki_balans': ['exact', 'gte', 'lte'],
            'aciqlama': ['exact', 'icontains'],

            'emeliyyat_uslubu': ['exact', 'icontains'],
            
            # 'tarix': ['exact', 'gte', 'lte'],
        }