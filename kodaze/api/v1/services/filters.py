import django_filters

from services.models import (
    Service,
    ServicePayment
)

class ServiceFilter(django_filters.FilterSet):
    contract__contract_date = django_filters.DateFilter(
        field_name='contract__contract_date', input_formats=["%d-%m-%Y"])
    contract__contract_date__gte = django_filters.DateFilter(
        field_name='contract__contract_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    contract__contract_date__lte = django_filters.DateFilter(
        field_name='contract__contract_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    service_date = django_filters.DateFilter(
        field_name='service_date', input_formats=["%d-%m-%Y"])
    service_date__gte = django_filters.DateFilter(
        field_name='service_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    service_date__lte = django_filters.DateFilter(
        field_name='service_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = Service
        fields = {
            'contract' : ['exact'],
            'contract__office__name': ['exact', 'icontains'],
            'contract__company__name': ['exact', 'icontains'],

            'contract__group_leader__fullname': ['exact', 'icontains'],
            'contract__group_leader__team__name': ['exact', 'icontains'],
            'contract__group_leader__employee_status__status_name': ['exact', 'icontains'],

            'contract__creditors__creditor': ['exact'],
            'contract__creditors__creditor__fullname': ['exact'],

            'contract__payment_style': ['exact'],
            'contract__contract_status': ['exact'],
            # 'contract__contract_date': ['exact', 'gte', 'lte'],
            'contract__total_amount': ['exact', 'gte', 'lte'],
            'contract__product_quantity': ['exact', 'gte', 'lte'],

            'contract__customer__fullname': ['exact', 'icontains'],
            'contract__customer__address': ['exact', 'icontains'],
            'contract__customer__phone_number_1': ['exact', 'icontains'],
            'contract__customer__phone_number_2': ['exact', 'icontains'],
            'contract__customer__phone_number_3': ['exact', 'icontains'],
            'contract__customer__phone_number_4': ['exact', 'icontains'],

            # 'service_date': ['exact', 'gte', 'lte'],
            'is_done': ['exact'],
            'confirmation': ['exact'],

        }

class ServicePaymentFilter(django_filters.FilterSet):
    service__contract__contract_date = django_filters.DateFilter(
        field_name='service__contract__contract_date', input_formats=["%d-%m-%Y"])
    service__contract__contract_date__gte = django_filters.DateFilter(
        field_name='service__contract__contract_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    service__contract__contract_date__lte = django_filters.DateFilter(
        field_name='service__contract__contract_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    service__service_date = django_filters.DateFilter(
        field_name='service__service_date', input_formats=["%d-%m-%Y"])
    service__service_date__gte = django_filters.DateFilter(
        field_name='service__service_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    service__service_date__lte = django_filters.DateFilter(
        field_name='service__service_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    payment_date = django_filters.DateFilter(
        field_name='payment_date', input_formats=["%d-%m-%Y"])
    payment_date__gte = django_filters.DateFilter(
        field_name='payment_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    payment_date__lte = django_filters.DateFilter(
        field_name='payment_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = ServicePayment
        fields = {
            'service' : ['exact'],
            'is_done': ['exact'],

            'total_amount_to_be_paid' : ['exact'],
            'amount_to_be_paid' : ['exact'],

            'service__installment' : ['exact'],
            'service__loan_term' : ['exact'],
            'service__discount' : ['exact'],
            'service__product' : ['exact'],
            'service__price' : ['exact'],

            'service__contract' : ['exact'],
            'service__contract__office__name': ['exact', 'icontains'],
            'service__contract__company__name': ['exact', 'icontains'],
            
            'service__contract__group_leader__fullname': ['exact', 'icontains'],
            'service__contract__group_leader__team__name': ['exact', 'icontains'],
            'service__contract__group_leader__employee_status__status_name': ['exact', 'icontains'],
            'service__contract__creditors__creditor': ['exact'],
            'service__contract__creditors__creditor__fullname': ['exact'],
            'service__contract__payment_style': ['exact'],
            'service__contract__contract_status': ['exact'],
            'service__contract__total_amount': ['exact', 'gte', 'lte'],
            'service__contract__product_quantity': ['exact', 'gte', 'lte'],
            'service__contract__customer__fullname': ['exact', 'icontains'],
            'service__contract__customer__address': ['exact', 'icontains'],
            'service__contract__customer__phone_number_1': ['exact', 'icontains'],
            'service__contract__customer__phone_number_2': ['exact', 'icontains'],
            'service__contract__customer__phone_number_3': ['exact', 'icontains'],
            'service__contract__customer__phone_number_4': ['exact', 'icontains'],
            'service__is_done': ['exact'],
            'service__confirmation': ['exact'],
        }
