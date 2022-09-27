import django_filters

from company.models import (
    Department,
    Company,
    Office,
    Team,
    Section,
    PermissionForPosition,
    Position
)

class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = {
            'name': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class DepartmentFilter(django_filters.FilterSet):
    class Meta:
        model = Department
        fields = {
            'name': ['exact', 'icontains'],
            'holding': ['exact'],
            'holding__id': ['exact'],
            'holding__name': ['exact', 'icontains'],
            'is_active': ['exact']
        }


class OfficeFilter(django_filters.FilterSet):
    class Meta:
        model = Office
        fields = {
            'name': ['exact', 'icontains'],
            'company': ['exact'],
            'company__id': ['exact'],
            'company__name': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class SectionFilter(django_filters.FilterSet):
    class Meta:
        model = Section
        fields = {
            'name': ['exact', 'icontains'],
            'office': ['exact'],
            'office__id': ['exact'],
            'office__name': ['exact', 'icontains'],
            'is_active': ['exact']
        }

class PositionFilter(django_filters.FilterSet):
    class Meta:
        model = Position
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'company': ['exact'],
            'company__id': ['exact'],
            'company__name': ['exact', 'icontains'],
            'is_active': ['exact']
        }

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
