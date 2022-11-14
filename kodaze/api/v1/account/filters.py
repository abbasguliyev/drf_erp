import django_filters

from account.models import (
    CustomerNote, 
    User, 
    Customer,
    Region,
    EmployeeStatus
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
    start_date_of_work = django_filters.DateFilter(field_name='start_date_of_work', input_formats=["%d-%m-%Y"])
    start_date_of_work__gte = django_filters.DateFilter(field_name='start_date_of_work', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    start_date_of_work__lte = django_filters.DateFilter(field_name='start_date_of_work', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    user_of_companies = django_filters.BooleanFilter(method="user_of_company", label="user_of_companies")
    user_of_holdings = django_filters.BooleanFilter(method="user_of_holding", label="user_of_holdings")


    class Meta:
        model = User
        fields = {
            'fullname': ['exact', 'icontains'],
            'position__name': ['exact', 'icontains'],
            'position': ['exact'],
            'is_superuser': ['exact'],

            'holding': ['exact'],
            'holding__name': ['exact', 'icontains'],
            'company': ['exact'],
            'company__name': ['exact', 'icontains'],
            'office': ['exact'],
            'office__name': ['exact', 'icontains'],
            'section': ['exact'],
            'section__name': ['exact', 'icontains'],
            'department': ['exact'],
            'department__name': ['exact', 'icontains'],
            'is_active': ['exact'],
            'employee_status': ['exact'],
            'employee_status__status_name': ['exact', 'icontains'],
        }

    def user_of_company(self, queryset, name, value):
        qs = None
        qs = queryset.filter(~Q(company=None))
        return qs

    def user_of_holding(self, queryset, name, value):
        qs = None
        qs = queryset.filter(Q(company=None, office=None))
        return qs

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

class CustomerNoteFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = CustomerNote
        fields = {
            'customer__fullname': ['exact', 'icontains'],
            'customer__phone_number_1': ['exact', 'icontains'],
            'customer__phone_number_2': ['exact', 'icontains'],
            'customer__phone_number_3': ['exact', 'icontains'],
            'customer__phone_number_4': ['exact', 'icontains'],
            'customer__region__region_name': ['exact', 'icontains'],
            'customer__region': ['exact'],
            'note': ['exact', 'icontains'],
            # 'date': ['exact', 'gte', 'lte'],
        }