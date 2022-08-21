import django_filters

from contract.models import (
    MuqavileHediyye, 
    Muqavile, 
    OdemeTarix,  
    DemoSatis
)

class OdemeTarixFilter(django_filters.FilterSet):
    muqavile__muqavile_tarixi = django_filters.DateFilter(field_name='muqavile__muqavile_tarixi', input_formats=["%d-%m-%Y"])
    muqavile__muqavile_tarixi__gte = django_filters.DateFilter(field_name='muqavile__muqavile_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    muqavile__muqavile_tarixi__lte = django_filters.DateFilter(field_name='muqavile__muqavile_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    tarix = django_filters.DateFilter(field_name='tarix', input_formats=["%d-%m-%Y"])
    tarix__gte = django_filters.DateFilter(field_name='tarix', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    tarix__lte = django_filters.DateFilter(field_name='tarix', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = OdemeTarix
        fields = {
            'muqavile' : ['exact'],
            'muqavile__shobe__shobe_adi': ['exact', 'icontains'],
            'muqavile__ofis__ofis_adi': ['exact', 'icontains'],
            'muqavile__shirket__shirket_adi': ['exact', 'icontains'],

            'muqavile__vanleader__asa': ['exact', 'icontains'],
            'muqavile__vanleader__komanda__komanda_adi': ['exact', 'icontains'],
            'muqavile__vanleader__isci_status__status_adi': ['exact', 'icontains'],

            'muqavile__odenis_uslubu': ['exact'],
            'muqavile__kreditor__kreditor': ['exact'],
            'muqavile__kreditor__kreditor__asa': ['exact'],
            'muqavile__muqavile_status': ['exact'],
            # 'muqavile__muqavile_tarixi': ['exact'],
            # 'muqavile__muqavile_tarixi': ['exact', 'gte', 'lte'],
            'muqavile__muqavile_umumi_mebleg': ['exact', 'gte', 'lte'],
            'muqavile__mehsul_sayi': ['exact', 'gte', 'lte'],

            'muqavile__musteri__asa': ['exact', 'icontains'],
            'muqavile__musteri__unvan': ['exact', 'icontains'],
            'muqavile__musteri__tel1': ['exact', 'icontains'],
            'muqavile__musteri__tel2': ['exact', 'icontains'],
            'muqavile__musteri__tel3': ['exact', 'icontains'],
            'muqavile__musteri__tel4': ['exact', 'icontains'],

            # 'tarix': ['exact'],
            # 'tarix': ['exact', 'gte', 'lte'],
            'qiymet': ['exact', 'gte', 'lte'],     
            'odenme_status': ['exact', 'icontains'],
            'gecikdirme_status': ['exact', 'icontains'],
            'buraxilmis_ay_alt_status': ['exact', 'icontains'],
            'natamam_ay_alt_status': ['exact', 'icontains'],
            'artiq_odeme_alt_status': ['exact', 'icontains'],
            'sertli_odeme_status': ['exact', 'icontains'],
            'borcu_bagla_status': ['exact', 'icontains'],
        }


class MuqavileFilter(django_filters.FilterSet):
    muqavile_tarixi = django_filters.DateFilter(field_name='muqavile_tarixi', input_formats=["%d-%m-%Y"])
    muqavile_tarixi__gte = django_filters.DateFilter(field_name='muqavile_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    muqavile_tarixi__lte = django_filters.DateFilter(field_name='muqavile_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    muqavile_imzalanma_tarixi = django_filters.DateFilter(field_name='muqavile_imzalanma_tarixi', input_formats=["%d-%m-%Y"])
    muqavile_imzalanma_tarixi__gte = django_filters.DateFilter(field_name='muqavile_imzalanma_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    muqavile_imzalanma_tarixi__lte = django_filters.DateFilter(field_name='muqavile_imzalanma_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    negd_odenis_1_tarix = django_filters.DateFilter(field_name='negd_odenis_1_tarix', input_formats=["%d-%m-%Y"])
    negd_odenis_1_tarix__gte = django_filters.DateFilter(field_name='negd_odenis_1_tarix', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    negd_odenis_1_tarix__lte = django_filters.DateFilter(field_name='negd_odenis_1_tarix', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    negd_odenis_2_tarix = django_filters.DateFilter(field_name='negd_odenis_2_tarix', input_formats=["%d-%m-%Y"])
    negd_odenis_2_tarix__gte = django_filters.DateFilter(field_name='negd_odenis_2_tarix', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    negd_odenis_2_tarix__lte = django_filters.DateFilter(field_name='negd_odenis_2_tarix', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    ilkin_odenis_tarixi = django_filters.DateFilter(field_name='ilkin_odenis_tarixi', input_formats=["%d-%m-%Y"])
    ilkin_odenis_tarixi__gte = django_filters.DateFilter(field_name='ilkin_odenis_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    ilkin_odenis_tarixi__lte = django_filters.DateFilter(field_name='ilkin_odenis_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    ilkin_odenis_qaliq_tarixi = django_filters.DateFilter(field_name='ilkin_odenis_qaliq_tarixi', input_formats=["%d-%m-%Y"])
    ilkin_odenis_qaliq_tarixi__gte = django_filters.DateFilter(field_name='ilkin_odenis_qaliq_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    ilkin_odenis_qaliq_tarixi__lte = django_filters.DateFilter(field_name='ilkin_odenis_qaliq_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = Muqavile
        fields = {
            'musteri__asa': ['exact', 'icontains'],
            'musteri__tel1': ['exact', 'icontains'],
            'musteri__tel2': ['exact', 'icontains'],
            'musteri__tel3': ['exact', 'icontains'],
            'musteri__tel4': ['exact', 'icontains'],
            'musteri__bolge__bolge_adi': ['exact', 'icontains'],
            'musteri__bolge': ['exact'],

            'kreditor__kreditor__asa': ['exact'],
            'kreditor__kreditor__id': ['exact'],

            # 'muqavile_tarixi': ['exact', 'gte', 'lte'],
            # 'muqavile_imzalanma_tarixi': ['exact', 'gte', 'lte'],

            'shirket__id': ['exact'],
            'shirket': ['exact'],
            'shirket__shirket_adi': ['exact', 'icontains'],
            'ofis': ['exact'],
            'ofis__id': ['exact'],
            'ofis__ofis_adi': ['exact', 'icontains'],

            'odenis_uslubu': ['exact', 'icontains'],
            'deyisilmis_mehsul_status': ['exact', 'icontains'],
            'muqavile_status': ['exact', 'icontains'],
            
            'negd_odenis_1': ['exact', 'gte', 'lte'],
            'negd_odenis_2': ['exact', 'gte', 'lte'],
            'negd_odenis_1_status': ['exact', 'icontains'],
            'negd_odenis_2_status': ['exact', 'icontains'],
            # 'negd_odenis_1_tarix': ['exact', 'gte', 'lte'],
            # 'negd_odenis_2_tarix': ['exact', 'gte', 'lte'],

            'yeni_qrafik_mebleg': ['exact', 'gte', 'lte'],
            'yeni_qrafik_status': ['exact', 'icontains'],
            
            'kredit_muddeti': ['exact', 'gte', 'lte'],
            
            'ilkin_odenis': ['exact', 'gte', 'lte'],
            'ilkin_odenis_qaliq': ['exact', 'gte', 'lte'],
            # 'ilkin_odenis_tarixi': ['exact', 'gte', 'lte'],
            # 'ilkin_odenis_qaliq_tarixi': ['exact', 'gte', 'lte'],
            'ilkin_odenis_status': ['exact', 'icontains'],
            'qaliq_ilkin_odenis_status': ['exact', 'icontains'],

            'vanleader__komanda': ['exact'],
            'vanleader__komanda__komanda_adi': ['exact', 'icontains'],
            'vanleader__asa': ['exact', 'icontains'],
            'vanleader__isci_status__status_adi': ['exact', 'icontains'],

            'dealer__asa': ['exact', 'icontains'],
            'dealer__isci_status__status_adi': ['exact', 'icontains'],

            'canvesser__asa': ['exact', 'icontains'],
            'canvesser__isci_status__status_adi': ['exact', 'icontains'],

            'mehsul_sayi': ['exact', 'gte', 'lte'],
            'mehsul__mehsulun_adi': ['exact', 'icontains'],
            'mehsul__qiymet': ['exact', 'gte', 'lte'],

            'muqavile_umumi_mebleg': ['exact', 'gte', 'lte'],

            'kompensasiya_medaxil': ['exact', 'gte', 'lte'],
            'kompensasiya_mexaric': ['exact', 'gte', 'lte'],

            'is_sokuntu': ['exact']
        }

class MuqavileHediyyeFilter(django_filters.FilterSet):
    muqavile__muqavile_tarixi = django_filters.DateFilter(field_name='muqavile__muqavile_tarixi', input_formats=["%d-%m-%Y"])
    muqavile__muqavile_tarixi__gte = django_filters.DateFilter(field_name='muqavile__muqavile_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    muqavile__muqavile_tarixi__lte = django_filters.DateFilter(field_name='muqavile__muqavile_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = MuqavileHediyye
        fields = {
            'mehsul__id': ['exact'],
            'mehsul__mehsulun_adi': ['exact', 'icontains'],
            'mehsul__qiymet': ['exact', 'gte', 'lte'],

            'muqavile' : ['exact'],
            'muqavile__shobe__shobe_adi': ['exact', 'icontains'],
            'muqavile__ofis__ofis_adi': ['exact', 'icontains'],
            'muqavile__shirket__shirket_adi': ['exact', 'icontains'],

            'muqavile__vanleader__asa': ['exact', 'icontains'],
            'muqavile__vanleader__komanda__komanda_adi': ['exact', 'icontains'],
            'muqavile__vanleader__isci_status__status_adi': ['exact', 'icontains'],


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
        }

class DemoSatisFilter(django_filters.FilterSet):
    created_date = django_filters.DateFilter(field_name='created_date', input_formats=["%d-%m-%Y"])
    created_date__gte = django_filters.DateFilter(field_name='created_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    created_date__lte = django_filters.DateFilter(field_name='created_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = DemoSatis
        fields = {
            'user': ['exact'],
            'user__asa': ['exact'],
            'user__shirket': ['exact'],
            'user__shirket__shirket_adi': ['exact', 'icontains'],
            'user__ofis': ['exact'],
            'user__ofis__ofis_adi': ['exact', 'icontains'],
            'user__vezife': ['exact'],
            'user__vezife__vezife_adi': ['exact', 'icontains'],
            'user__komanda': ['exact'],
            'user__komanda__komanda_adi': ['exact', 'icontains'],
            # 'created_date': ['exact', 'gte', 'lte'],
        }