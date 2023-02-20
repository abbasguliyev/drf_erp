import django_filters

from django.db.models import Q

from contract.models import (
    ContractGift, 
    Contract, 
    Installment,  
    DemoSales,
)

class ContractCreditorFilter(django_filters.FilterSet):
    class Meta:
        fields = {
            'contract' : ['exact'],
            'creditor' : ['exact']
        }

class InstallmentFilter(django_filters.FilterSet):
    contract__contract_date = django_filters.DateFilter(field_name='contract__contract_date', input_formats=["%d-%m-%Y"])
    contract__contract_date__gte = django_filters.DateFilter(field_name='contract__contract_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    contract__contract_date__lte = django_filters.DateFilter(field_name='contract__contract_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    date = django_filters.DateFilter(field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    customer_phone_number = django_filters.CharFilter(method="customer_phone_number_filter", label="customer_phone_number")

    def customer_phone_number_filter(self, queryset, name, value):
        qs = None
        for term in value.split():
            qs = queryset.filter(
                Q(contract__customer__phone_number_1__icontains=term) | Q(contract__customer__phone_number_2__icontains=term) | Q(contract__customer__phone_number_3__icontains=term) | Q(contract__customer__phone_number_4__icontains=term))
        return qs

    class Meta:
        model = Installment
        fields = {
            'contract' : ['exact'],
            'contract__is_holding_contract': ['exact'],
            'contract__office': ['exact'],
            'contract__company': ['exact'],

            'contract__group_leader': ['exact'],
            'contract__group_leader__employee_status__status_name': ['exact', 'icontains'],

            'contract__payment_style': ['exact'],
            'contract__creditors__creditor': ['exact'],
            'contract__creditors__creditor__fullname': ['exact'],
            'contract__contract_status': ['exact'],
            'contract__total_amount': ['exact', 'gte', 'lte'],
            'contract__product_quantity': ['exact', 'gte', 'lte'],

            'contract__customer': ['exact'],
            'contract__customer__fullname': ['exact', 'icontains'],
            'contract__customer__address': ['exact', 'icontains'],
            'contract__customer__region': ['exact'],

            'price': ['exact', 'gte', 'lte'],
            'is_paid': ['exact'],
            'payment_status': ['exact', 'icontains'],
            'close_the_debt_status': ['exact', 'icontains']
        }


class ContractFilter(django_filters.FilterSet):
    contract_date = django_filters.DateFilter(field_name='contract_date', input_formats=["%d-%m-%Y"])
    contract_date__gte = django_filters.DateFilter(field_name='contract_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    contract_date__lte = django_filters.DateFilter(field_name='contract_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    intervention_date = django_filters.DateFilter(field_name='intervention_date', input_formats=["%d-%m-%Y"])
    intervention_date__gte = django_filters.DateFilter(field_name='intervention_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    intervention_date__lte = django_filters.DateFilter(field_name='intervention_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    initial_payment_date = django_filters.DateFilter(field_name='initial_payment_date', input_formats=["%d-%m-%Y"])
    initial_payment_date__gte = django_filters.DateFilter(field_name='initial_payment_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    initial_payment_date__lte = django_filters.DateFilter(field_name='initial_payment_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    initial_payment_debt_date = django_filters.DateFilter(field_name='initial_payment_debt_date', input_formats=["%d-%m-%Y"])
    initial_payment_debt_date__gte = django_filters.DateFilter(field_name='initial_payment_debt_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    initial_payment_debt_date__lte = django_filters.DateFilter(field_name='initial_payment_debt_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    customer_phone_number = django_filters.CharFilter(method="customer_phone_number_filter", label="customer_phone_number")
    sales_worker = django_filters.NumberFilter(method="sales_worker_filter", label="sales_worker")

    without_changed_contract = django_filters.BooleanFilter(method="without_changed_contract_filter", label="without_changed_contract")

    def without_changed_contract_filter(self, queryset, name, value):
        qs = None
        qs = queryset.filter(~Q(cancelled_contract=True))
        return qs

    def customer_phone_number_filter(self, queryset, name, value):
        qs = None
        for term in value.split():
            qs = queryset.filter(
                Q(customer__phone_number_1__icontains=term) | Q(customer__phone_number_2__icontains=term) | Q(customer__phone_number_3__icontains=term) | Q(customer__phone_number_4__icontains=term))
        return qs

    def sales_worker_filter(self, queryset, name, value):
        qs = None
        qs = queryset.filter(Q(group_leader=value) | Q(manager1=value) | Q(manager2=value))
        return qs

    class Meta:
        model = Contract
        fields = {
            'is_holding_contract': ['exact'],
            
            'customer': ['exact'],
            'customer__fullname': ['exact', 'icontains'],
            'customer__region': ['exact'],
            'customer__region__region_name': ['exact', 'icontains'],
            
            'company': ['exact'],
            'company__name': ['exact', 'icontains'],
            'office': ['exact'],
            'office__name': ['exact', 'icontains'],
            
            'payment_style': ['exact', 'icontains'],
            'is_conditional_contract': ['exact'],

            'contract_date': ['exact', 'month', 'year'],

            'creditors__creditor__fullname': ['exact'],
            'creditors__creditor__id': ['exact'],

            'intervention_product_status': ['exact', 'icontains'],
            'contract_status': ['exact', 'icontains'],
            
            'loan_term': ['exact', 'gte', 'lte'],
            
            'initial_payment': ['exact', 'gte', 'lte'],
            'initial_payment_debt': ['exact', 'gte', 'lte'],
            'initial_payment_status': ['exact', 'icontains'],
            'initial_payment_debt_status': ['exact', 'icontains'],

            'group_leader': ['exact'],
            'group_leader__fullname': ['exact', 'icontains'],
            'group_leader__employee_status__status_name': ['exact', 'icontains'],

            'manager1': ['exact'],
            'manager1__fullname': ['exact', 'icontains'],
            'manager1__employee_status__status_name': ['exact', 'icontains'],

            'manager2': ['exact'],
            'manager2__fullname': ['exact', 'icontains'],
            'manager2__employee_status__status_name': ['exact', 'icontains'],

            'product_quantity': ['exact', 'gte', 'lte'],
            'product': ['exact'],
            'product__product_name': ['exact', 'icontains'],
            'product__price': ['exact', 'gte', 'lte'],

            'total_amount': ['exact', 'gte', 'lte'],

            'compensation_income': ['exact', 'gte', 'lte'],
            'compensation_expense': ['exact', 'gte', 'lte'],

            'region': ['exact'],
            'address': ['exact', 'icontains'],
        }

class ContractGiftFilter(django_filters.FilterSet):
    contract__contract_date = django_filters.DateFilter(field_name='contract__contract_date', input_formats=["%d-%m-%Y"])
    contract__contract_date__gte = django_filters.DateFilter(field_name='contract__contract_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    contract__contract_date__lte = django_filters.DateFilter(field_name='contract__contract_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = ContractGift
        fields = {
            'product': ['exact'],
            'contract' : ['exact'],
            'contract__customer': ['exact'],
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