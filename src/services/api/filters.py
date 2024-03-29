import django_filters

from services.models import (
    Service,
    ServicePayment,
    ServiceProductForContract
)

from django.db.models import Q

class ServiceFilter(django_filters.FilterSet):
    create_date = django_filters.DateFilter(field_name='create_date', input_formats=["%d-%m-%Y"])
    create_date__gte = django_filters.DateFilter(field_name='create_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    create_date__lte = django_filters.DateFilter(field_name='create_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    service_date = django_filters.DateFilter(field_name='service_date', input_formats=["%d-%m-%Y"])
    service_date__gte = django_filters.DateFilter(field_name='service_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    service_date__lte = django_filters.DateFilter(field_name='service_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    appointment_date = django_filters.DateFilter(field_name='appointment_date', input_formats=["%d-%m-%Y"])
    appointment_date__gte = django_filters.DateFilter(field_name='appointment_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    appointment_date__lte = django_filters.DateFilter(field_name='appointment_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    phone_number = django_filters.CharFilter(method="phone_number_filter", label="phone_number")

    class Meta:
        model = Service
        fields = {
            'product': ['exact'],
            'product__product_name': ['exact', 'icontains'],
            'customer': ['exact'],
            'customer__region': ['exact'],
            'customer__region__region_name': ['exact', 'icontains'],
            'customer': ['exact'],
            'customer__fullname': ['exact', 'icontains'],
            'customer__address': ['exact', 'icontains'],
            
            'pay_method': ['exact'],

            'contract': ['exact'],
            'contract__office': ['exact'],
            'contract__company': ['exact'],

            'contract__group_leader': ['exact'],
            'contract__creditors__creditor': ['exact'],

            'contract__payment_style': ['exact'],
            'contract__contract_status': ['exact'],
            'contract__total_amount': ['exact', 'gte', 'lte'],
            'contract__product_quantity': ['exact', 'gte', 'lte'],

            'service_creditor': ['exact'],
            'operator': ['exact'],

            'is_done': ['exact'],
        }

    def phone_number_filter(self, queryset, name, value):
        qs = None
        for term in value.split():
            qs = queryset.filter(
                Q(customer__phone_number_1__icontains=term) | Q(customer__phone_number_2__icontains=term) | Q(customer__phone_number_3__icontains=term) | Q(customer__phone_number_4__icontains=term))
        return qs


class ServicePaymentFilter(django_filters.FilterSet):
    service__service_date = django_filters.DateFilter(
        field_name='service__service_date', input_formats=["%d-%m-%Y"])
    service__service_date__gte = django_filters.DateFilter(
        field_name='service__service_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    service__service_date__lte = django_filters.DateFilter(
        field_name='service__service_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    service__appointment_date = django_filters.DateFilter(
        field_name='service__appointment_date', input_formats=["%d-%m-%Y"])
    service__appointment_date__gte = django_filters.DateFilter(
        field_name='service__appointment_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    service__appointment_date__lte = django_filters.DateFilter(
        field_name='service__appointment_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    payment_date = django_filters.DateFilter(
        field_name='payment_date', input_formats=["%d-%m-%Y"])
    payment_date__gte = django_filters.DateFilter(
        field_name='payment_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    payment_date__lte = django_filters.DateFilter(
        field_name='payment_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    is_holding = django_filters.BooleanFilter(method="is_holding_filter", label="is_holding")

    def is_holding_filter(self, queryset, name, value):
        qs = None
        if value == True:
            qs = queryset.filter(
                Q(service__contract__is_holding_contract=True) | Q(service__contract=None) 
            )
        elif value == False:
            qs = queryset.filter(
                Q(service__contract__is_holding_contract=False) | ~Q(service__contract__company=None) 
            )
        else:
            qs = queryset
        return qs

    class Meta:
        model = ServicePayment
        fields = {
            'service': ['exact'],
            'is_done': ['exact'],

            'service_amount': ['exact'],
            'service__is_done': ['exact'],
            'service__service_creditor': ['exact'],
            'service__customer': ['exact'],
            'service__customer__fullname': ['exact', 'icontains'],
            'service__customer__region': ['exact'],
            'service__contract__is_holding_contract': ['exact'],
            'service__contract__company': ['exact'],
            'service__contract__office': ['exact'],
        }

class ServiceProductForContractFilter(django_filters.FilterSet):
    class Meta:
        model = ServiceProductForContract
        fields = {
            'company': ['exact'],
            'service_period': ['exact'],
            'product': ['exact'],
        }