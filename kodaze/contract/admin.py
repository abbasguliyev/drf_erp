from django.contrib import admin
from .models import (
    Contract,
    ContractGift, 
    Installment, 
    ContractChange, 
    DemoSales, 
    ContractCreditor
)
class InstallmentAdmin(admin.ModelAdmin):
    list_filter = [
        "contract",
        'contract__payment_style',
        'payment_status',
        'delay_status',
        'missed_month_substatus',
        'incomplete_month_substatus',
    ]
    search_fields = (
        "contract",
    )

# Register your models here.
admin.site.register(Contract)
admin.site.register(ContractGift)
admin.site.register(ContractChange)
admin.site.register(Installment, InstallmentAdmin)
admin.site.register(DemoSales)
admin.site.register(ContractCreditor)