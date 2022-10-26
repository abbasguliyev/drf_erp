from django.contrib import admin
from .models import (
    Contract,
    ContractGift, 
    Installment, 
    ContractChange, 
    DemoSales, 
    ContractCreditor
)

@admin.register(Installment)
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
    list_display = (
        'month_no', 
        'contract', 
        'price', 
        'payment_status', 
        'date',
        'conditional_payment_status', 
        'close_the_debt_status',
        'delay_status',
        'missed_month_substatus',
        'incomplete_month_substatus',
        'overpayment_substatus'
    )

# Register your models here.
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_filter = [
        'group_leader',
        'manager1',
        'manager2',
        'customer',
        'product',
        'product_quantity',
        'total_amount',
        'contract_date',
        'payment_style',
        'contract_status',
        'office',
        'remaining_debt',
        'is_remove',
        'loan_term',
        'initial_payment',
        'initial_payment_debt',
        'initial_payment_date',
        'initial_payment_debt_date',
        'initial_payment_status',
        'initial_payment_debt_status',
        'cancelled_date',
        'debt_closing_date',
        'compensation_income',
        'compensation_expense',
        'note',
        'new_graphic_amount',
        'new_graphic_status',
        'modified_product_status',
    ]
    search_fields = (
        'customer',
    )
    list_display = (
        'id',
        'group_leader',
        'manager1',
        'manager2',
        'customer',
        'product',
        'product_quantity',
        'total_amount',
        'contract_date',
        'payment_style',
        'contract_status',
        'office',
        'remaining_debt',
        'is_remove',
        'loan_term',
        'initial_payment',
        'initial_payment_debt',
        'initial_payment_date',
        'initial_payment_debt_date',
        'initial_payment_status',
        'initial_payment_debt_status',
        'cancelled_date',
        'debt_closing_date',
        'compensation_income',
        'compensation_expense',
        'note',
        'new_graphic_amount',
        'new_graphic_status',
        'modified_product_status',
    )

@admin.register(ContractGift)
class ContractGiftAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "contract", "quantity", "gift_date")
    list_display_links = ("id",)

admin.site.register(ContractChange)

@admin.register(DemoSales)
class DemoSalesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "count", "created_date", "sale_count")
    list_display_links = ("id",)

@admin.register(ContractCreditor)
class ContractCreditorAdmin(admin.ModelAdmin):
    list_display = ("id", "creditor", "contract")
    list_display_links = ("id",)