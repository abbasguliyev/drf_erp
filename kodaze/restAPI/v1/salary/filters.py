import django_filters

from salary.models import (
    Avans,
    Menecer1PrimNew,
    Kesinti,
    Bonus,
    MaasGoruntuleme,
    MaasOde,
    GroupLeaderPrim,
    Menecer1Prim,
    OfficeLeaderPrim,
    Menecer2Prim,
    GroupLeaderPrimNew
)


class AvansFilter(django_filters.FilterSet):
    avans_tarixi = django_filters.DateFilter(
        field_name='avans_tarixi', input_formats=["%d-%m-%Y"])
    avans_tarixi__gte = django_filters.DateFilter(
        field_name='avans_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    avans_tarixi__lte = django_filters.DateFilter(
        field_name='avans_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = Avans
        fields = {
            'isci__asa': ['exact', 'icontains'],
            'isci__vezife__vezife_adi': ['exact', 'icontains'],
            'isci__isci_status__status_adi': ['exact', 'icontains'],

            'mebleg': ['exact', 'gte', 'lte'],
            'yarim_ay_emek_haqqi': ['exact', 'gte', 'lte'],

            'qeyd': ['exact', 'icontains'],
            # 'avans_tarixi': ['exact', 'gte', 'lte'],
        }


class KesintiFilter(django_filters.FilterSet):
    kesinti_tarixi = django_filters.DateFilter(
        field_name='kesinti_tarixi', input_formats=["%d-%m-%Y"])
    kesinti_tarixi__gte = django_filters.DateFilter(
        field_name='kesinti_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    kesinti_tarixi__lte = django_filters.DateFilter(
        field_name='kesinti_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = Kesinti
        fields = {
            'isci__asa': ['exact', 'icontains'],
            'isci__vezife__vezife_adi': ['exact', 'icontains'],
            'isci__isci_status__status_adi': ['exact', 'icontains'],

            'mebleg': ['exact', 'gte', 'lte'],

            'qeyd': ['exact', 'icontains'],
            # 'kesinti_tarixi': ['exact', 'gte', 'lte'],
        }


class BonusFilter(django_filters.FilterSet):
    bonus_tarixi = django_filters.DateFilter(
        field_name='bonus_tarixi', input_formats=["%d-%m-%Y"])
    bonus_tarixi__gte = django_filters.DateFilter(
        field_name='bonus_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    bonus_tarixi__lte = django_filters.DateFilter(
        field_name='bonus_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = Bonus
        fields = {
            'isci__asa': ['exact', 'icontains'],
            'isci__vezife__vezife_adi': ['exact', 'icontains'],
            'isci__isci_status__status_adi': ['exact', 'icontains'],

            'mebleg': ['exact', 'gte', 'lte'],

            'qeyd': ['exact', 'icontains'],
            # 'bonus_tarixi': ['exact', 'gte', 'lte'],
        }


class MaasGoruntulemeFilter(django_filters.FilterSet):
    tarix = django_filters.DateFilter(
        field_name='tarix', input_formats=["%d-%m-%Y"])
    tarix__gte = django_filters.DateFilter(
        field_name='tarix', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    tarix__lte = django_filters.DateFilter(
        field_name='tarix', lookup_expr='lte', input_formats=["%d-%m-%Y"])

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

            # 'tarix': ['exact', 'gte', 'lte', 'month', 'year'],
        }


class MaasOdeFilter(django_filters.FilterSet):
    odeme_tarixi = django_filters.DateFilter(
        field_name='odeme_tarixi', input_formats=["%d-%m-%Y"])
    odeme_tarixi__gte = django_filters.DateFilter(
        field_name='odeme_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    odeme_tarixi__lte = django_filters.DateFilter(
        field_name='odeme_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = MaasOde
        fields = {
            'isci__asa': ['exact', 'icontains'],
            'isci__id': ['exact', 'icontains'],
            'isci__vezife__vezife_adi': ['exact', 'icontains'],
            'isci__isci_status__status_adi': ['exact', 'icontains'],

            'mebleg': ['exact', 'gte', 'lte'],

            'qeyd': ['exact', 'icontains'],
            # 'odeme_tarixi': ['exact', 'gte', 'lte'],
        }


class GroupLeaderPrimFilter(django_filters.FilterSet):
    class Meta:
        model = GroupLeaderPrim
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


class GroupLeaderPrimNewFilter(django_filters.FilterSet):
    class Meta:
        model = GroupLeaderPrimNew
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


class Menecer1PrimFilter(django_filters.FilterSet):
    class Meta:
        model = Menecer1Prim
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


class Menecer1PrimNewFilter(django_filters.FilterSet):
    class Meta:
        model = Menecer1PrimNew
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


class Menecer2PrimFilter(django_filters.FilterSet):
    class Meta:
        model = Menecer2Prim
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
