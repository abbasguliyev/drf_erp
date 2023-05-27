from django.contrib import admin
from .models import (
    Contract,
    ContractGift, 
    Installment, 
    DemoSales, 
    ContractCreditor
)

@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_filter = [
        "contract",
        'contract__payment_style',
        'close_the_debt_status',
        'payment_status',
        'delay_status',
    ]
    search_fields = (
        "contract",
    )
    list_display = (
        'id',
        'is_paid',
        'month_no', 
        'contract', 
        'price', 
        'paid_price', 
        'payment_status',
        'date',
        'paid_date',
        'delay_status',
        'remaining_debt',
        'last_month'
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
        'default_installment_amount',
        'loan_term',
        'initial_payment',
        'initial_payment_debt',
        'initial_payment_date',
        'initial_payment_debt_date',
        'initial_payment_status',
        'initial_payment_debt_status',
        'intervention_date',
        'debt_closing_date',
        'compensation_income',
        'compensation_expense',
        'note',
        'intervention_product_status'
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
        'discount',
        'contract_date',
        'payment_style',
        'contract_status',
        'office',
        'remaining_debt',
        'default_installment_amount',
        'loan_term',
        'initial_payment',
        'initial_payment_debt',
        'initial_payment_date',
        'initial_payment_debt_date',
        'initial_payment_status',
        'initial_payment_debt_status',
        'intervention_date',
        'debt_closing_date',
        'compensation_income',
        'compensation_expense',
        'note',
        'intervention_product_status',
        'changed_new_contract',
        'cancelled_contract'
    )

@admin.register(ContractGift)
class ContractGiftAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "contract", "quantity", "gift_date")
    list_display_links = ("id",)

@admin.register(DemoSales)
class DemoSalesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "count", "created_date", "sale_count")
    list_display_links = ("id",)

@admin.register(ContractCreditor)
class ContractCreditorAdmin(admin.ModelAdmin):
    list_display = ("id", "creditor", "contract")
    list_display_links = ("id",)