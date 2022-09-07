import django_filters

from services.models import (
    Servis,
    ServisOdeme
)

class ServisFilter(django_filters.FilterSet):
    muqavile__muqavile_tarixi = django_filters.DateFilter(
        field_name='muqavile__muqavile_tarixi', input_formats=["%d-%m-%Y"])
    muqavile__muqavile_tarixi__gte = django_filters.DateFilter(
        field_name='muqavile__muqavile_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    muqavile__muqavile_tarixi__lte = django_filters.DateFilter(
        field_name='muqavile__muqavile_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    servis_tarix = django_filters.DateFilter(
        field_name='servis_tarix', input_formats=["%d-%m-%Y"])
    servis_tarix__gte = django_filters.DateFilter(
        field_name='servis_tarix', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    servis_tarix__lte = django_filters.DateFilter(
        field_name='servis_tarix', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = Servis
        fields = {
            'muqavile' : ['exact'],
            'muqavile__shobe__shobe_adi': ['exact', 'icontains'],
            'muqavile__ofis__ofis_adi': ['exact', 'icontains'],
            'muqavile__shirket__shirket_adi': ['exact', 'icontains'],

            'muqavile__group_leader__asa': ['exact', 'icontains'],
            'muqavile__group_leader__komanda__komanda_adi': ['exact', 'icontains'],
            'muqavile__group_leader__isci_status__status_adi': ['exact', 'icontains'],

            'muqavile__kreditor__kreditor': ['exact'],
            'muqavile__kreditor__kreditor__asa': ['exact'],

            'muqavile__odenis_uslubu': ['exact'],
            'muqavile__muqavile_status': ['exact'],
            # 'muqavile__muqavile_tarixi': ['exact', 'gte', 'lte'],
            'muqavile__muqavile_umumi_mebleg': ['exact', 'gte', 'lte'],
            'muqavile__mehsul_sayi': ['exact', 'gte', 'lte'],

            'muqavile__musteri__asa': ['exact', 'icontains'],
            'muqavile__musteri__unvan': ['exact', 'icontains'],
            'muqavile__musteri__tel1': ['exact', 'icontains'],
            'muqavile__musteri__tel2': ['exact', 'icontains'],
            'muqavile__musteri__tel3': ['exact', 'icontains'],
            'muqavile__musteri__tel4': ['exact', 'icontains'],

            # 'servis_tarix': ['exact', 'gte', 'lte'],
            'yerine_yetirildi': ['exact'],
            'operator_tesdiq': ['exact'],

        }

class ServisOdemeFilter(django_filters.FilterSet):
    servis__muqavile__muqavile_tarixi = django_filters.DateFilter(
        field_name='servis__muqavile__muqavile_tarixi', input_formats=["%d-%m-%Y"])
    servis__muqavile__muqavile_tarixi__gte = django_filters.DateFilter(
        field_name='servis__muqavile__muqavile_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    servis__muqavile__muqavile_tarixi__lte = django_filters.DateFilter(
        field_name='servis__muqavile__muqavile_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    servis__servis_tarix = django_filters.DateFilter(
        field_name='servis__servis_tarix', input_formats=["%d-%m-%Y"])
    servis__servis_tarix__gte = django_filters.DateFilter(
        field_name='servis__servis_tarix', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    servis__servis_tarix__lte = django_filters.DateFilter(
        field_name='servis__servis_tarix', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    odeme_tarix = django_filters.DateFilter(
        field_name='odeme_tarix', input_formats=["%d-%m-%Y"])
    odeme_tarix__gte = django_filters.DateFilter(
        field_name='odeme_tarix', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    odeme_tarix__lte = django_filters.DateFilter(
        field_name='odeme_tarix', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = ServisOdeme
        fields = {
            'servis' : ['exact'],
            'odendi': ['exact'],

            'odenilecek_umumi_mebleg' : ['exact'],
            'odenilecek_mebleg' : ['exact'],

            'servis__kredit' : ['exact'],
            'servis__kredit_muddeti' : ['exact'],
            'servis__endirim' : ['exact'],
            'servis__mehsullar' : ['exact'],
            'servis__servis_qiymeti' : ['exact'],

            'servis__muqavile' : ['exact'],
            'servis__muqavile__shobe__shobe_adi': ['exact', 'icontains'],
            'servis__muqavile__ofis__ofis_adi': ['exact', 'icontains'],
            'servis__muqavile__shirket__shirket_adi': ['exact', 'icontains'],
            
            'servis__muqavile__group_leader__asa': ['exact', 'icontains'],
            'servis__muqavile__group_leader__komanda__komanda_adi': ['exact', 'icontains'],
            'servis__muqavile__group_leader__isci_status__status_adi': ['exact', 'icontains'],
            'servis__muqavile__kreditor__kreditor': ['exact'],
            'servis__muqavile__kreditor__kreditor__asa': ['exact'],
            'servis__muqavile__odenis_uslubu': ['exact'],
            'servis__muqavile__muqavile_status': ['exact'],
            # 'servis__muqavile__muqavile_tarixi': ['exact', 'gte', 'lte'],
            'servis__muqavile__muqavile_umumi_mebleg': ['exact', 'gte', 'lte'],
            'servis__muqavile__mehsul_sayi': ['exact', 'gte', 'lte'],
            'servis__muqavile__musteri__asa': ['exact', 'icontains'],
            'servis__muqavile__musteri__unvan': ['exact', 'icontains'],
            'servis__muqavile__musteri__tel1': ['exact', 'icontains'],
            'servis__muqavile__musteri__tel2': ['exact', 'icontains'],
            'servis__muqavile__musteri__tel3': ['exact', 'icontains'],
            'servis__muqavile__musteri__tel4': ['exact', 'icontains'],

            # 'servis__servis_tarix': ['exact', 'gte', 'lte'],
            'servis__yerine_yetirildi': ['exact'],
            'servis__operator_tesdiq': ['exact'],

            # 'odeme_tarix': ['exact', 'gte', 'lte'],
        }
