import django_filters
from django.db.models import Q


from salary.models import (
    AdvancePayment,
    SalaryDeduction,
    Bonus,
    SalaryPunishment,
    SalaryView,
    PaySalary,
    EmployeeActivityHistory
)

class DateYearMonthFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    year = django_filters.CharFilter(method="year_filter", label="year")
    month = django_filters.CharFilter(method="month_filter", label="month")
    
    def year_filter(self, queryset, name, value):
        qs = self.queryset.filter(Q(date__year=value))
        return qs
    def month_filter(self, queryset, name, value):
        qs = self.queryset.filter(Q(date__month=value))
        return qs


class AdvancePaymentFilter(DateYearMonthFilter):
    class Meta:
        model = AdvancePayment
        fields = {
            'employee': ['exact'],
            'employee__fullname': ['exact', 'icontains'],
            'amount': ['exact', 'icontains'],
            'note': ['exact', 'icontains'],
        }


class SalaryDeductionFilter(DateYearMonthFilter):
    class Meta:
        model = SalaryDeduction
        fields = {
            'employee': ['exact'],
            'employee__fullname': ['exact', 'icontains'],
            'amount': ['exact', 'icontains'],
            'note': ['exact', 'icontains'],
        }

class SalaryPunishmentFilter(DateYearMonthFilter):
    class Meta:
        model = SalaryPunishment
        fields = {
            'employee': ['exact'],
            'employee__fullname': ['exact', 'icontains'],
            'amount': ['exact', 'icontains'],
            'note': ['exact', 'icontains'],
        }


class BonusFilter(DateYearMonthFilter):
    class Meta:
        model = Bonus
        fields = {
            'employee': ['exact'],
            'employee__fullname': ['exact', 'icontains'],
            'amount': ['exact', 'icontains'],
            'note': ['exact', 'icontains'],
        }

class SalaryViewFilter(DateYearMonthFilter):
    class Meta:
        model = SalaryView
        fields = {
            'employee': ['exact'],
            'employee__fullname': ['exact', 'icontains'],
            'employee__is_superuser': ['exact'],

            'employee__office': ['exact'],
            'employee__office__id': ['exact'],
            'employee__office__name': ['exact', 'icontains'],

            'employee__company': ['exact'],
            'employee__company__id': ['exact'],
            'employee__company__name': ['exact', 'icontains'],

            'employee__position': ['exact'],
            'employee__position__id': ['exact'],
            'employee__position__name': ['exact', 'icontains'],

            'employee__employee_status': ['exact'],
            'employee__employee_status__status_name': ['exact', 'icontains'],

            'is_done': ['exact'],

            'sale_quantity': ['exact', 'gte', 'lte'],
            'sales_amount': ['exact', 'gte', 'lte'],
            'final_salary': ['exact', 'gte', 'lte'],
        }


class PaySalaryFilter(DateYearMonthFilter):
    class Meta:
        model = PaySalary
        fields = {
            'employee__fullname': ['exact', 'icontains'],
            'employee__id': ['exact', 'icontains'],
            'employee__position__name': ['exact', 'icontains'],
            'employee__employee_status__status_name': ['exact', 'icontains'],
            'amount': ['exact', 'gte', 'lte'],
            'note': ['exact', 'icontains'],
        }

class EmployeeActivityHistoryFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='activity_date', lookup_expr='gte', input_formats=["%d-%m-%Y"], label='start_date')
    end_date = django_filters.DateFilter(
        field_name='activity_date', lookup_expr='lte', input_formats=["%d-%m-%Y"], label='end_date')

    class Meta:
        model = EmployeeActivityHistory
        fields = {
            'salary_view__employee__id': ['exact'],
            'salary_view__final_salary': ['exact'],
            'salary_view__sale_quantity': ['exact'],
            'bonus': ['exact'],
            'advance_payment': ['exact'],
            'salary_deduction': ['exact'],
            'salary_punishment': ['exact'],
        }
