import django_filters

from account.models import (
    User, 
    Customer,
    Region,
    EmployeeStatus
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
        }

class EmployeeStatusFilter(django_filters.FilterSet):
    class Meta:
        model = EmployeeStatus
        fields = {
            'status_name': ['exact', 'icontains'],
        }

class RegionFilter(django_filters.FilterSet):
    class Meta:
        model = Region
        fields = {
            'region_name': ['exact', 'icontains'],
        }

class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = {
            'fullname': ['exact', 'icontains'],
            'phone_number_1': ['exact', 'icontains'],
            'phone_number_2': ['exact', 'icontains'],
            'phone_number_3': ['exact', 'icontains'],
            'phone_number_4': ['exact', 'icontains'],
            'is_active': ['exact'],
            'address': ['exact', 'icontains'],
            'region__region_name': ['exact', 'icontains'],
        }