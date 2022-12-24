from django.contrib import admin
from .models import (
    Service, 
    ServicePayment, 
    ServiceProductForContract
)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "id", "contract", "create_date", "appointment_date",
        "service_date", "customer", "pay_method", "loan_term",
        "price", "total_paid_amount", "remaining_payment", "discount",
        "is_done", "is_auto"
    )
    list_filter = [
        "contract", "create_date", "appointment_date",
        "service_date", "customer", "product", "pay_method", "loan_term",
        "price", "total_paid_amount", "remaining_payment", "discount",
        "is_done", "is_auto"
    ]
    search_fields = (
        "contract",
    )

@admin.register(ServicePayment)
class ServicePaymentAdmin(admin.ModelAdmin):
    list_display = [
        "service", "service_amount", "payment_date", "is_done"
    ]
    list_filter = [
        "service", "service_amount", "payment_date", "is_done"
    ]
    search_fields = (
        "service",
    )

@admin.register(ServiceProductForContract)
class ServiceProductForContractAdmin(admin.ModelAdmin):
    list_display = [
        "company", "product", "service_period"
    ]
    list_filter = [
        "company", "product", "service_period"
    ]
