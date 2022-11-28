import django_filters
from holiday.models import (
    EmployeeWorkingDay,
    EmployeeHolidayHistory,
    EmployeeHoliday
)

class EmployeeWorkingDayFilter(django_filters.FilterSet):
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"], label="start_date")
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"], label="end_date")

    class Meta:
        model = EmployeeWorkingDay
        fields = {
            'employee': ['exact'],
            'employee__fullname': ['exact', 'icontains'],
            'employee__company': ['exact'],
            'employee__office': ['exact'],
            'employee__position': ['exact'],
        }

class EmployeeHolidayHistoryFilter(django_filters.FilterSet):
    created_date__gte = django_filters.DateFilter(
        field_name='created_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    created_date__lte = django_filters.DateFilter(
        field_name='created_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = EmployeeHolidayHistory
        fields = ('created_date',)

class EmployeeHolidayFilter(django_filters.FilterSet):
    holiday_date__gte = django_filters.DateFilter(
        field_name='holiday_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    holiday_date__lte = django_filters.DateFilter(
        field_name='holiday_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = EmployeeHoliday
        fields = {
            'employee': ['exact'],
            'history': ['exact']
        }