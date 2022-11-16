import django_filters
import datetime
from django.db.models import Count, Q, Sum


from salary.models import (
    AdvancePayment,
    SalaryDeduction,
    Bonus,
    SalaryPunishment,
    SalaryView,
    PaySalary,
)


class AdvancePaymentFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = AdvancePayment
        fields = {
            'employee__fullname': ['exact', 'icontains'],
            'employee__position__name': ['exact', 'icontains'],
            'employee__employee_status__status_name': ['exact', 'icontains'],
            'note': ['exact', 'icontains'],
        }


class SalaryDeductionFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = SalaryDeduction
        fields = {
            'employee__fullname': ['exact', 'icontains'],
            'employee__position__name': ['exact', 'icontains'],
            'employee__employee_status__status_name': ['exact', 'icontains'],

            'amount': ['exact', 'gte', 'lte'],

            'note': ['exact', 'icontains'],
        }


class SalaryPunishmentFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = SalaryPunishment
        fields = {
            'employee__fullname': ['exact', 'icontains'],
            'employee__position__name': ['exact', 'icontains'],
            'employee__employee_status__status_name': ['exact', 'icontains'],

            'amount': ['exact', 'gte', 'lte'],

            'note': ['exact', 'icontains'],
        }


class BonusFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = Bonus
        fields = {
            'employee__fullname': ['exact', 'icontains'],
            'employee__position__name': ['exact', 'icontains'],
            'employee__employee_status__status_name': ['exact', 'icontains'],

            'amount': ['exact', 'gte', 'lte'],

            'note': ['exact', 'icontains'],
            # 'date': ['exact', 'gte', 'lte'],
        }


class SalaryViewFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = SalaryView
        fields = {
            'employee__fullname': ['exact', 'icontains'],

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


class PaySalaryFilter(django_filters.FilterSet):
    installment = django_filters.DateFilter(
        field_name='installment', input_formats=["%d-%m-%Y"])
    installment__gte = django_filters.DateFilter(
        field_name='installment', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    installment__lte = django_filters.DateFilter(
        field_name='installment', lookup_expr='lte', input_formats=["%d-%m-%Y"])

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
