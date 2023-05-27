import django_filters

from account.models import (
    User, 
    Customer,
    Region,
    EmployeeStatus,
    EmployeeActivity
)
from django.contrib.auth.models import Permission, Group
from django.db.models import Q


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
    contract_date = django_filters.DateFilter(field_name='contract_date', input_formats=["%d-%m-%Y"])
    contract_date__gte = django_filters.DateFilter(field_name='contract_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    contract_date__lte = django_filters.DateFilter(field_name='contract_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = User
        fields = {
            'fullname': ['exact', 'icontains'],
            'position__name': ['exact', 'icontains', 'in'],
            'position': ['exact'],
            'is_superuser': ['exact'],
            'salary_style': ['exact'],

            'register_type': ['exact'],
            'company': ['exact'],
            'company__name': ['exact', 'icontains'],
            'office': ['exact'],
            'office__name': ['exact', 'icontains'],
            'department': ['exact'],
            'department__name': ['exact', 'icontains'],
            'is_active': ['exact'],
            'employee_status': ['exact'],
            'employee_status__status_name': ['exact', 'icontains'],
            'fin_code': ['exact'],
        }

class EmployeeStatusFilter(django_filters.FilterSet):
    class Meta:
        model = EmployeeStatus
        fields = {
            'status_name': ['exact', 'icontains'],
        }

class EmployeeActivityFilter(django_filters.FilterSet):
    class Meta:
        model = EmployeeActivity
        fields = {
            'employee': ['exact'],
        }

class RegionFilter(django_filters.FilterSet):
    class Meta:
        model = Region
        fields = {
            'region_name': ['exact', 'icontains'],
        }

class CustomerFilter(django_filters.FilterSet):
    phone_number = django_filters.CharFilter(method="phone_number_filter", label="phone_number")
    def phone_number_filter(self, queryset, name, value):
        qs = None
        for term in value.split():
            qs = queryset.filter(
                Q(phone_number_1__icontains=term) | Q(phone_number_2__icontains=term) | Q(phone_number_3__icontains=term) | Q(phone_number_4__icontains=term))
        return qs
    class Meta:
        model = Customer
        fields = {
            'fullname': ['exact', 'icontains'],
            'is_active': ['exact'],
            'address': ['exact', 'icontains'],
            'region__region_name': ['exact', 'icontains'],
            'fin_code': ['exact'],
        }
