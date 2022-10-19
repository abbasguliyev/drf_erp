import django_filters

from income_expense.models import (
    HoldingCashboxIncome,
    HoldingCashboxExpense,
    OfficeCashboxIncome,
    OfficeCashboxExpense,
    CompanyCashboxIncome,
    CompanyCashboxExpense,
)

class HoldingCashboxIncomeFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
   
    class Meta:
        model = HoldingCashboxIncome
        fields = {
            'executor__fullname': ['exact', 'icontains'],
            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'cashbox__holding__name': ['exact', 'icontains'],
            'amount': ['exact', 'gte', 'lte'],
            'note': ['exact', 'icontains'],
            
            # 'date': ['exact', 'gte', 'lte'],

        }

class HoldingCashboxExpenseFilter(django_filters.FilterSet):
    expense_datei = django_filters.DateFilter(field_name='expense_datei', input_formats=["%d-%m-%Y"])
    expense_datei__gte = django_filters.DateFilter(field_name='expense_datei', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    expense_datei__lte = django_filters.DateFilter(field_name='expense_datei', lookup_expr='lte', input_formats=["%d-%m-%Y"])
   
    class Meta:
        model = HoldingCashboxExpense
        fields = {
            'executor__fullname': ['exact', 'icontains'],
            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'cashbox__holding__name': ['exact', 'icontains'],
            'amount': ['exact', 'gte', 'lte'],
            'note': ['exact', 'icontains'],
            
            # 'expense_datei': ['exact', 'gte', 'lte'],
        }

class CompanyCashboxIncomeFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
   
    class Meta:
        model = CompanyCashboxIncome
        fields = {
            'executor__fullname': ['exact', 'icontains'],
            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'cashbox__company__name': ['exact', 'icontains'],
            'amount': ['exact', 'gte', 'lte'],
            'note': ['exact', 'icontains'],
            
            # 'date': ['exact', 'gte', 'lte'],

        }

class CompanyCashboxExpenseFilter(django_filters.FilterSet):
    expense_datei = django_filters.DateFilter(field_name='expense_datei', input_formats=["%d-%m-%Y"])
    expense_datei__gte = django_filters.DateFilter(field_name='expense_datei', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    expense_datei__lte = django_filters.DateFilter(field_name='expense_datei', lookup_expr='lte', input_formats=["%d-%m-%Y"])
   
    class Meta:
        model = CompanyCashboxExpense
        fields = {
            'executor__fullname': ['exact', 'icontains'],
            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'cashbox__company__name': ['exact', 'icontains'],
            'amount': ['exact', 'gte', 'lte'],
            'note': ['exact', 'icontains'],
            
            # 'expense_datei': ['exact', 'gte', 'lte'],
        }

class OfficeCashboxIncomeFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
   
    class Meta:
        model = OfficeCashboxIncome
        fields = {
            'executor__fullname': ['exact', 'icontains'],
            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'cashbox__office__name': ['exact', 'icontains'],
            'amount': ['exact', 'gte', 'lte'],
            'note': ['exact', 'icontains'],
            
            # 'date': ['exact', 'gte', 'lte'],

        }

class OfficeCashboxExpenseFilter(django_filters.FilterSet):
    expense_datei = django_filters.DateFilter(field_name='expense_datei', input_formats=["%d-%m-%Y"])
    expense_datei__gte = django_filters.DateFilter(field_name='expense_datei', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    expense_datei__lte = django_filters.DateFilter(field_name='expense_datei', lookup_expr='lte', input_formats=["%d-%m-%Y"])
   
    class Meta:
        model = OfficeCashboxExpense
        fields = {
            'executor__fullname': ['exact', 'icontains'],
            'executor__position__name': ['exact', 'icontains'],
            'executor__employee_status__status_name': ['exact', 'icontains'],

            'cashbox__office__name': ['exact', 'icontains'],
            'amount': ['exact', 'gte', 'lte'],
            'note': ['exact', 'icontains'],
            
            # 'expense_datei': ['exact', 'gte', 'lte'],
        }
