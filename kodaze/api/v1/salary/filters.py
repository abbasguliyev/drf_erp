import django_filters

from salary.models import (
    AdvancePayment,
    Manager1PrimNew,
    SalaryDeduction,
    Bonus,
    SalaryPunishment,
    SalaryView,
    PaySalary,
    OfficeLeaderPrim,
    Manager2Prim,
    GroupLeaderPrimNew
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

            'employee__employee_status__status_name': ['exact', 'icontains'],

            'employee__team': ['exact'],
            'employee__team_id': ['exact'],
            'employee__team__name': ['exact', 'icontains'],

            'is_done': ['exact'],

            'sale_quantity': ['exact', 'gte', 'lte'],
            'sales_amount': ['exact', 'gte', 'lte'],
            'final_salary': ['exact', 'gte', 'lte'],

            # 'date': ['exact', 'gte', 'lte', 'month', 'year'],
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
            # 'installment': ['exact', 'gte', 'lte'],
        }



class GroupLeaderPrimNewFilter(django_filters.FilterSet):
    class Meta:
        model = GroupLeaderPrimNew
        fields = {
            'prim_status__status_name': ['exact', 'icontains'],
            'sales_amount': ['exact', 'icontains'],

            'cash': ['exact'],
            'installment_4_12': ['exact'],
            'installment_13_18': ['exact'],
            'installment_19_24': ['exact'],

            'position__name': ['exact', 'icontains'],

            'product__id': ['exact'],
            'product__product_name': ['exact', 'icontains'],
            'product__price': ['exact', 'gte', 'lte'],
        }



class Manager1PrimNewFilter(django_filters.FilterSet):
    class Meta:
        model = Manager1PrimNew
        fields = {
            'prim_status__status_name': ['exact', 'icontains'],
            'sales_amount': ['exact', 'icontains'],

            'cash': ['exact'],
            'installment_4_12': ['exact'],
            'installment_13_18': ['exact'],
            'installment_19_24': ['exact'],

            'position__name': ['exact', 'icontains'],

            'product__id': ['exact'],
            'product__product_name': ['exact', 'icontains'],
            'product__price': ['exact', 'gte', 'lte']
        }


class OfficeLeaderPrimFilter(django_filters.FilterSet):
    class Meta:
        model = OfficeLeaderPrim
        fields = {
            'prim_status__status_name': ['exact', 'icontains'],
            'sales_amount': ['exact', 'icontains'],

            'position__name': ['exact', 'icontains'],

            'product__id': ['exact'],
            'product__product_name': ['exact', 'icontains'],
            'product__price': ['exact', 'gte', 'lte'],

            'prim_for_office': ['exact', 'gte', 'lte'],
            'fix_prim': ['exact', 'gte', 'lte'],
        }


class Manager2PrimFilter(django_filters.FilterSet):
    class Meta:
        model = Manager2Prim
        fields = {
            'prim_status__status_name': ['exact', 'icontains'],
            'sales_amount': ['exact', 'icontains'],

            'position__name': ['exact', 'icontains'],

            'product__id': ['exact'],
            'product__product_name': ['exact', 'icontains'],
            'product__price': ['exact', 'gte', 'lte'],

            'prim_for_office': ['exact', 'gte', 'lte'],
            'fix_prim': ['exact', 'gte', 'lte'],
            'sale0': ['exact', 'gte', 'lte'],
            'sale1_8': ['exact', 'gte', 'lte'],
            'sale9_14': ['exact', 'gte', 'lte'],
            'sale15p': ['exact', 'gte', 'lte'],
            'sale20p': ['exact', 'gte', 'lte'],
            'prim_for_team': ['exact', 'gte', 'lte']
        }
