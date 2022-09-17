import django_filters

from company.models import (
    Department,
    Shirket,
    Ofis,
    Komanda,
    Shobe,
    VezifePermission,
    Vezifeler
)

class ShirketFilter(django_filters.FilterSet):
    class Meta:
        model = Shirket
        fields = {
            'shirket_adi': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class DepartmentFilter(django_filters.FilterSet):
    class Meta:
        model = Department
        fields = {
            'departament_adi': ['exact', 'icontains'],
            'shirket__id': ['exact'],
            'shirket__shirket_adi': ['exact', 'icontains'],
            'is_active': ['exact']
        }


class OfisFilter(django_filters.FilterSet):
    class Meta:
        model = Ofis
        fields = {
            'ofis_adi': ['exact', 'icontains'],
            'shirket__id': ['exact'],
            'shirket__shirket_adi': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class ShobeFilter(django_filters.FilterSet):
    class Meta:
        model = Shobe
        fields = {
            'shobe_adi': ['exact', 'icontains'],
            'ofis': ['exact'],
            'ofis__id': ['exact'],
            'ofis__ofis_adi': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class VezifeFilter(django_filters.FilterSet):
    class Meta:
        model = Vezifeler
        fields = {
            'id': ['exact'],
            'vezife_adi': ['exact', 'icontains'],
            'shirket__id': ['exact'],
            'shirket__shirket_adi': ['exact', 'icontains'],
            'shobe__id': ['exact'],
            'shobe__shobe_adi': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class KomandaFilter(django_filters.FilterSet):
    class Meta:
        model = Komanda
        fields = {
            'komanda_adi': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class VezifePermissionFilter(django_filters.FilterSet):
    class Meta:
        model = VezifePermission
        fields = {
            'vezife__vezife_adi': ['exact', 'icontains']
        }
