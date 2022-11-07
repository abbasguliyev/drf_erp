import django_filters
from django.db import models
from django.db.models import Q, Count
from company.models import (
    Department,
    Company,
    Office,
    Team,
    Section,
    PermissionForPosition,
    Position
)

from django.contrib.auth import get_user_model

User = get_user_model()

def user_count_filter(self, queryset, name, value):
    qs = None
    qs = queryset.annotate(user_count=Count("employees")).filter(user_count=value)
    return qs

class CompanyFilter(django_filters.FilterSet):
    employee_count = django_filters.NumberFilter(method="company_user_count_filter", label="employee_count")
    
    class Meta:
        model = Company
        fields = {
            'name': ['exact', 'icontains'],
            'is_active': ['exact'],
        }

    def company_user_count_filter(self, queryset, name, value):
        return user_count_filter(self, queryset, name, value)


class DepartmentFilter(django_filters.FilterSet):
    employee_count = django_filters.NumberFilter(method="department_user_count_filter", label="employee_count")

    class Meta:
        model = Department
        fields = {
            'name': ['exact', 'icontains'],
            'is_active': ['exact'],
        }

    def department_user_count_filter(self, queryset, name, value):
        return user_count_filter(self, queryset, name, value)


class OfficeFilter(django_filters.FilterSet):
    employee_count = django_filters.NumberFilter(method="office_user_count_filter", label="employee_count")


    class Meta:
        model = Office
        fields = {
            'name': ['exact', 'icontains'],
            'company': ['exact'],
            'company__id': ['exact'],
            'company__name': ['exact', 'icontains'],
            'is_active': ['exact']
        }

    def office_user_count_filter(self, queryset, name, value):
        return user_count_filter(self, queryset, name, value)

class SectionFilter(django_filters.FilterSet):
    employee_count = django_filters.NumberFilter(method="section_user_count_filter", label="employee_count")

    class Meta:
        model = Section
        fields = {
            'name': ['exact', 'icontains'],
            'is_active': ['exact']
        }

    def section_user_count_filter(self, queryset, name, value):
        return user_count_filter(self, queryset, name, value)

class PositionFilter(django_filters.FilterSet):
    employee_count = django_filters.NumberFilter(method="position_user_count_filter", label="employee_count")

    class Meta:
        model = Position
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'is_active': ['exact']
        }

    def position_user_count_filter(self, queryset, name, value):
        return user_count_filter(self, queryset, name, value)

class TeamFilter(django_filters.FilterSet):
    class Meta:
        model = Team
        fields = {
            'name': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class PermissionForPositionFilter(django_filters.FilterSet):
    class Meta:
        model = PermissionForPosition
        fields = {
            'position__name': ['exact', 'icontains'],
            'permission_group__name': ['exact', 'icontains']
        }
