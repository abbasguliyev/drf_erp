from django.contrib import admin
from cashbox.models import (
    OfficeCashbox,
    CompanyCashbox,
    HoldingCashbox,
    CashFlow,
    CostType
)

@admin.register(OfficeCashbox)
class OfficeCashboxAdmin(admin.ModelAdmin):
    list_display = ('office', 'balance')
    list_filter = ['office', 'balance']

@admin.register(CompanyCashbox)
class CompanyCashboxAdmin(admin.ModelAdmin):
    list_display = ('company', 'balance')
    list_filter = ['company', 'balance']

@admin.register(HoldingCashbox)
class HoldingCashboxAdmin(admin.ModelAdmin):
    list_display = ('holding', 'balance')
    list_filter = ['holding', 'balance']

@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date', 
        'holding', 
        'company', 
        'office',
        'description',
        'balance',
        'executor',
        'personal',
        'operation_style',
        'quantity'
    )
    list_filter = [
        'id',
        'date', 
        'holding', 
        'company', 
        'office',
        'description',
        'balance',
        'executor',
        'personal',
        'operation_style',
        'quantity'
    ]

@admin.register(CostType)
class CostTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ['name']
