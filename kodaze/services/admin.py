from django.contrib import admin
from .models import (
    Service, 
    ServicePayment, 
)

class ServiceAdmin(admin.ModelAdmin):
    list_filter = [
        "contract",
    ]
    search_fields = (
        "contract",
    )

class ServicePaymentAdmin(admin.ModelAdmin):
    list_filter = [
        "service",
    ]
    search_fields = (
        "service",
    )

admin.site.register(Service, ServiceAdmin)
admin.site.register(ServicePayment, ServicePaymentAdmin)