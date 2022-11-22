import django_filters

from contract.models import (
    ContractGift, 
    Contract, 
    Installment,  
    DemoSales
)

class InstallmentFilter(django_filters.FilterSet):
    contract__contract_date = django_filters.DateFilter(field_name='contract__contract_date', input_formats=["%d-%m-%Y"])
    contract__contract_date__gte = django_filters.DateFilter(field_name='contract__contract_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    contract__contract_date__lte = django_filters.DateFilter(field_name='contract__contract_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    date = django_filters.DateFilter(field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = Installment
        fields = {
            'contract' : ['exact'],
            'contract__office__name': ['exact', 'icontains'],
            'contract__company__name': ['exact', 'icontains'],

            'contract__group_leader__fullname': ['exact', 'icontains'],
            'contract__group_leader__employee_status__status_name': ['exact', 'icontains'],

            'contract__payment_style': ['exact'],
            'contract__creditors__creditor': ['exact'],
            'contract__creditors__creditor__fullname': ['exact'],
            'contract__contract_status': ['exact'],
            'contract__total_amount': ['exact', 'gte', 'lte'],
            'contract__product_quantity': ['exact', 'gte', 'lte'],

            'contract__customer__fullname': ['exact', 'icontains'],
            'contract__customer__address': ['exact', 'icontains'],
            'contract__customer__phone_number_1': ['exact', 'icontains'],
            'contract__customer__phone_number_2': ['exact', 'icontains'],
            'contract__customer__phone_number_3': ['exact', 'icontains'],
            'contract__customer__phone_number_4': ['exact', 'icontains'],

            'price': ['exact', 'gte', 'lte'],
            'payment_status': ['exact', 'icontains'],
            'delay_status': ['exact', 'icontains'],
            'missed_month_substatus': ['exact', 'icontains'],
            'incomplete_month_substatus': ['exact', 'icontains'],
            'overpayment_substatus': ['exact', 'icontains'],
            'conditional_payment_status': ['exact', 'icontains'],
            'close_the_debt_status': ['exact', 'icontains'],
        }


class ContractFilter(django_filters.FilterSet):
    contract_date = django_filters.DateFilter(field_name='contract_date', input_formats=["%d-%m-%Y"])
    contract_date__gte = django_filters.DateFilter(field_name='contract_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    contract_date__lte = django_filters.DateFilter(field_name='contract_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    contract_created_date = django_filters.DateFilter(field_name='contract_created_date', input_formats=["%d-%m-%Y"])
    contract_created_date__gte = django_filters.DateFilter(field_name='contract_created_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    contract_created_date__lte = django_filters.DateFilter(field_name='contract_created_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    initial_payment_date = django_filters.DateFilter(field_name='initial_payment_date', input_formats=["%d-%m-%Y"])
    initial_payment_date__gte = django_filters.DateFilter(field_name='initial_payment_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    initial_payment_date__lte = django_filters.DateFilter(field_name='initial_payment_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    initial_payment_debt_date = django_filters.DateFilter(field_name='initial_payment_debt_date', input_formats=["%d-%m-%Y"])
    initial_payment_debt_date__gte = django_filters.DateFilter(field_name='initial_payment_debt_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    initial_payment_debt_date__lte = django_filters.DateFilter(field_name='initial_payment_debt_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = Contract
        fields = {
            'customer__fullname': ['exact', 'icontains'],
            'customer__phone_number_1': ['exact', 'icontains'],
            'customer__phone_number_2': ['exact', 'icontains'],
            'customer__phone_number_3': ['exact', 'icontains'],
            'customer__phone_number_4': ['exact', 'icontains'],
            'customer__region__region_name': ['exact', 'icontains'],
            'customer__region': ['exact'],

            'creditors__creditor__fullname': ['exact'],
            'creditors__creditor__id': ['exact'],

            'company__id': ['exact'],
            'company': ['exact'],
            'company__name': ['exact', 'icontains'],
            'office': ['exact'],
            'office__id': ['exact'],
            'office__name': ['exact', 'icontains'],

            'payment_style': ['exact', 'icontains'],
            'modified_product_status': ['exact', 'icontains'],
            'contract_status': ['exact', 'icontains'],

            'new_graphic_amount': ['exact', 'gte', 'lte'],
            'new_graphic_status': ['exact', 'icontains'],
            
            'loan_term': ['exact', 'gte', 'lte'],
            
            'initial_payment': ['exact', 'gte', 'lte'],
            'initial_payment_debt': ['exact', 'gte', 'lte'],
            'initial_payment_status': ['exact', 'icontains'],
            'initial_payment_debt_status': ['exact', 'icontains'],

            'group_leader__fullname': ['exact', 'icontains'],
            'group_leader__employee_status__status_name': ['exact', 'icontains'],

            'manager1__fullname': ['exact', 'icontains'],
            'manager1__employee_status__status_name': ['exact', 'icontains'],

            'manager2__fullname': ['exact', 'icontains'],
            'manager2__employee_status__status_name': ['exact', 'icontains'],

            'product_quantity': ['exact', 'gte', 'lte'],
            'product__product_name': ['exact', 'icontains'],
            'product__price': ['exact', 'gte', 'lte'],

            'total_amount': ['exact', 'gte', 'lte'],

            'compensation_income': ['exact', 'gte', 'lte'],
            'compensation_expense': ['exact', 'gte', 'lte'],

            'is_remove': ['exact']
        }

class ContractGiftFilter(django_filters.FilterSet):
    contract__contract_date = django_filters.DateFilter(field_name='contract__contract_date', input_formats=["%d-%m-%Y"])
    contract__contract_date__gte = django_filters.DateFilter(field_name='contract__contract_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    contract__contract_date__lte = django_filters.DateFilter(field_name='contract__contract_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = ContractGift
        fields = {
            'product__id': ['exact'],
            'product__product_name': ['exact', 'icontains'],
            'product__price': ['exact', 'gte', 'lte'],

            'contract' : ['exact'],
            'contract__office__name': ['exact', 'icontains'],
            'contract__company__name': ['exact', 'icontains'],

            'contract__group_leader__fullname': ['exact', 'icontains'],
            'contract__group_leader__employee_status__status_name': ['exact', 'icontains'],


            'contract__payment_style': ['exact'],
            'contract__contract_status': ['exact'],
            'contract__total_amount': ['exact', 'gte', 'lte'],
            'contract__product_quantity': ['exact', 'gte', 'lte'],

            'contract__customer__fullname': ['exact', 'icontains'],
            'contract__customer__address': ['exact', 'icontains'],
            'contract__customer__phone_number_1': ['exact', 'icontains'],
            'contract__customer__phone_number_2': ['exact', 'icontains'],
            'contract__customer__phone_number_3': ['exact', 'icontains'],
            'contract__customer__phone_number_4': ['exact', 'icontains'],
        }

class DemoSalesFilter(django_filters.FilterSet):
    created_date = django_filters.DateFilter(field_name='created_date', input_formats=["%d-%m-%Y"])
    created_date__gte = django_filters.DateFilter(field_name='created_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    created_date__lte = django_filters.DateFilter(field_name='created_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = DemoSales
        fields = {
            'user': ['exact'],
            'user__fullname': ['exact'],
            'user__company': ['exact'],
            'user__company__name': ['exact', 'icontains'],
            'user__office': ['exact'],
            'user__office__name': ['exact', 'icontains'],
            'user__position': ['exact'],
            'user__position__name': ['exact', 'icontains'],
        }