import django_filters

from account.models import (
    MusteriQeydler, 
    User, 
    Musteri,
    Bolge,
    IsciStatus
)

from django.contrib.auth.models import Permission, Group

class PermissionFilter(django_filters.FilterSet):
    class Meta:
        model = Permission
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'content_type': ['exact'],
            'codename': ['exact', 'icontains']
        }

class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = Group
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'permissions': ['exact', 'icontains']
        }

class UserFilter(django_filters.FilterSet):
    ishe_baslama_tarixi = django_filters.DateFilter(field_name='ishe_baslama_tarixi', input_formats=["%d-%m-%Y"])
    ishe_baslama_tarixi__gte = django_filters.DateFilter(field_name='ishe_baslama_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    ishe_baslama_tarixi__lte = django_filters.DateFilter(field_name='ishe_baslama_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = User
        fields = {
            'asa': ['exact', 'icontains'],
            'vezife__vezife_adi': ['exact', 'icontains'],
            'vezife': ['exact'],
            'is_superuser': ['exact'],

            'shirket__shirket_adi': ['exact', 'icontains'],
            'ofis__ofis_adi': ['exact', 'icontains'],
            'shobe__shobe_adi': ['exact', 'icontains'],
            'department__departament_adi': ['exact', 'icontains'],
            # 'ishe_baslama_tarixi': ['exact', 'gte', 'lte'],
            'is_active': ['exact'],
            'isci_status__status_adi': ['exact', 'icontains'],
        }

class IsciStatusFilter(django_filters.FilterSet):
    class Meta:
        model = IsciStatus
        fields = {
            'status_adi': ['exact', 'icontains'],
        }

class BolgeFilter(django_filters.FilterSet):
    class Meta:
        model = Bolge
        fields = {
            'bolge_adi': ['exact', 'icontains'],
        }

class MusteriFilter(django_filters.FilterSet):
    class Meta:
        model = Musteri
        fields = {
            'asa': ['exact', 'icontains'],
            'tel1': ['exact', 'icontains'],
            'tel2': ['exact', 'icontains'],
            'tel3': ['exact', 'icontains'],
            'tel4': ['exact', 'icontains'],
            'is_active': ['exact'],
            'unvan': ['exact', 'icontains'],
            'bolge__bolge_adi': ['exact', 'icontains'],
        }

class MusteriQeydlerFilter(django_filters.FilterSet):
    tarix = django_filters.DateFilter(field_name='tarix', input_formats=["%d-%m-%Y"])
    tarix__gte = django_filters.DateFilter(field_name='tarix', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    tarix__lte = django_filters.DateFilter(field_name='tarix', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = MusteriQeydler
        fields = {
            'musteri__asa': ['exact', 'icontains'],
            'musteri__tel1': ['exact', 'icontains'],
            'musteri__tel2': ['exact', 'icontains'],
            'musteri__tel3': ['exact', 'icontains'],
            'musteri__tel4': ['exact', 'icontains'],
            'musteri__bolge__bolge_adi': ['exact', 'icontains'],
            'musteri__bolge': ['exact'],
            'qeyd': ['exact', 'icontains'],
            # 'tarix': ['exact', 'gte', 'lte'],
        }