import django_filters

from salary.models import (
    Avans,
    DealerPrimNew,
    Kesinti,
    Bonus,
    MaasGoruntuleme,
    MaasOde, 
    VanLeaderPrim, 
    DealerPrim, 
    OfficeLeaderPrim,
    CanvasserPrim,
    VanLeaderPrimNew
)

class AvansFilter(django_filters.FilterSet):
    class Meta:
        model = Avans
        fields = {
            'isci__asa': ['exact', 'icontains'],
            'isci__vezife__vezife_adi': ['exact', 'icontains'],
            'isci__isci_status__status_adi': ['exact', 'icontains'],

            'mebleg': ['exact', 'gte', 'lte'],
            'yarim_ay_emek_haqqi': ['exact', 'gte', 'lte'],

            'qeyd': ['exact', 'icontains'],
            'avans_tarixi': ['exact', 'gte', 'lte'],
        }

class KesintiFilter(django_filters.FilterSet):
    class Meta:
        model = Kesinti
        fields = {
            'isci__asa': ['exact', 'icontains'],
            'isci__vezife__vezife_adi': ['exact', 'icontains'],
            'isci__isci_status__status_adi': ['exact', 'icontains'],

            'mebleg': ['exact', 'gte', 'lte'],

            'qeyd': ['exact', 'icontains'],
            'kesinti_tarixi': ['exact', 'gte', 'lte'],
        }

class BonusFilter(django_filters.FilterSet):
    class Meta:
        model = Bonus
        fields = {
            'isci__asa': ['exact', 'icontains'],
            'isci__vezife__vezife_adi': ['exact', 'icontains'],
            'isci__isci_status__status_adi': ['exact', 'icontains'],

            'mebleg': ['exact', 'gte', 'lte'],

            'qeyd': ['exact', 'icontains'],
            'bonus_tarixi': ['exact', 'gte', 'lte'],
        }

class MaasGoruntulemeFilter(django_filters.FilterSet):
    class Meta:
        model = MaasGoruntuleme
        fields = {
            'isci__asa': ['exact', 'icontains'],

            'isci__is_superuser': ['exact'],


            'isci__ofis': ['exact'],
            'isci__ofis__id': ['exact'],
            'isci__ofis__ofis_adi': ['exact', 'icontains'],
            
            'isci__shirket': ['exact'],
            'isci__shirket__id': ['exact'],
            'isci__shirket__shirket_adi': ['exact', 'icontains'],
            
            'isci__vezife': ['exact'],
            'isci__vezife__id': ['exact'],
            'isci__vezife__vezife_adi': ['exact', 'icontains'],
            
            'isci__isci_status__status_adi': ['exact', 'icontains'],

            'isci__komanda': ['exact'],
            'isci__komanda_id': ['exact'],
            'isci__komanda__komanda_adi': ['exact', 'icontains'],

            'odendi': ['exact'],

            'satis_sayi': ['exact', 'gte', 'lte'],
            'satis_meblegi': ['exact', 'gte', 'lte'],
            'yekun_maas': ['exact', 'gte', 'lte'],

            'tarix': ['exact', 'gte', 'lte', 'month', 'year'],
        }

class MaasOdeFilter(django_filters.FilterSet):
    class Meta:
        model = MaasOde
        fields = {
            'isci__asa': ['exact', 'icontains'],
            'isci__id': ['exact', 'icontains'],
            'isci__vezife__vezife_adi': ['exact', 'icontains'],
            'isci__isci_status__status_adi': ['exact', 'icontains'],

            'mebleg': ['exact', 'gte', 'lte'],

            'qeyd': ['exact', 'icontains'],
            'odeme_tarixi': ['exact', 'gte', 'lte'],
        }

class VanLeaderPrimFilter(django_filters.FilterSet):
    class Meta:
        model = VanLeaderPrim
        fields = {
            'prim_status__status_adi': ['exact', 'icontains'],
            'satis_meblegi': ['exact', 'icontains'],
            'odenis_uslubu': ['exact', 'gte', 'lte'],

            'vezife__vezife_adi': ['exact', 'icontains'],

            'mehsul__id': ['exact'],
            'mehsul__mehsulun_adi': ['exact', 'icontains'],
            'mehsul__qiymet': ['exact', 'gte', 'lte'],

            'komandaya_gore_prim': ['exact', 'gte', 'lte'],
            'fix_maas': ['exact', 'gte', 'lte'],
        }

class VanLeaderPrimNewFilter(django_filters.FilterSet):
    class Meta:
        model = VanLeaderPrimNew
        fields = {
            'prim_status__status_adi': ['exact', 'icontains'],
            'satis_meblegi': ['exact', 'icontains'],

            'negd': ['exact'],
            'kredit_4_12': ['exact'],
            'kredit_13_18': ['exact'],
            'kredit_19_24': ['exact'],

            'vezife__vezife_adi': ['exact', 'icontains'],

            'mehsul__id': ['exact'],
            'mehsul__mehsulun_adi': ['exact', 'icontains'],
            'mehsul__qiymet': ['exact', 'gte', 'lte'],
        }

class DealerPrimFilter(django_filters.FilterSet):
    class Meta:
        model = DealerPrim
        fields = {
            'prim_status__status_adi': ['exact', 'icontains'],
            'satis_meblegi': ['exact', 'icontains'],
            'odenis_uslubu': ['exact', 'gte', 'lte'],

            'vezife__vezife_adi': ['exact', 'icontains'],

            'mehsul__id': ['exact'],
            'mehsul__mehsulun_adi': ['exact', 'icontains'],
            'mehsul__qiymet': ['exact', 'gte', 'lte'],

            'komandaya_gore_prim': ['exact', 'gte', 'lte'],
            'fix_maas': ['exact', 'gte', 'lte'],
        }

class DealerPrimNewFilter(django_filters.FilterSet):
    class Meta:
        model = DealerPrimNew
        fields = {
            'prim_status__status_adi': ['exact', 'icontains'],
            'satis_meblegi': ['exact', 'icontains'],

            'negd': ['exact'],
            'kredit_4_12': ['exact'],
            'kredit_13_18': ['exact'],
            'kredit_19_24': ['exact'],

            'vezife__vezife_adi': ['exact', 'icontains'],

            'mehsul__id': ['exact'],
            'mehsul__mehsulun_adi': ['exact', 'icontains'],
            'mehsul__qiymet': ['exact', 'gte', 'lte']
        }


class OfficeLeaderPrimFilter(django_filters.FilterSet):
    class Meta:
        model = OfficeLeaderPrim
        fields = {
            'prim_status__status_adi': ['exact', 'icontains'],
            'satis_meblegi': ['exact', 'icontains'],

            'vezife__vezife_adi': ['exact', 'icontains'],

            'mehsul__id': ['exact'],
            'mehsul__mehsulun_adi': ['exact', 'icontains'],
            'mehsul__qiymet': ['exact', 'gte', 'lte'],

            'ofise_gore_prim': ['exact', 'gte', 'lte'],
            'fix_maas': ['exact', 'gte', 'lte'],
        }


class CanvasserPrimFilter(django_filters.FilterSet):
    class Meta:
        model = CanvasserPrim
        fields = {
            'prim_status__status_adi': ['exact', 'icontains'],
            'satis_meblegi': ['exact', 'icontains'],

            'vezife__vezife_adi': ['exact', 'icontains'],

            'mehsul__id': ['exact'],
            'mehsul__mehsulun_adi': ['exact', 'icontains'],
            'mehsul__qiymet': ['exact', 'gte', 'lte'],

            'ofise_gore_prim': ['exact', 'gte', 'lte'],
            'fix_maas': ['exact', 'gte', 'lte'],
            'satis0': ['exact', 'gte', 'lte'],
            'satis1_8': ['exact', 'gte', 'lte'],
            'satis9_14': ['exact', 'gte', 'lte'],
            'satis15p': ['exact', 'gte', 'lte'],
            'satis20p': ['exact', 'gte', 'lte'],
            'komandaya_gore_prim': ['exact', 'gte', 'lte']
        }