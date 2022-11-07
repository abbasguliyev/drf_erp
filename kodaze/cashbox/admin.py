from django.contrib import admin
from cashbox.models import (
    OfficeCashbox,
    CompanyCashbox,
    HoldingCashbox,
    CashFlow
)
# Register your models here.
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
        'initial_balance',
        'subsequent_balance',
        'holding_initial_balance',
        'holding_subsequent_balance',
        'company_initial_balance',
        'company_subsequent_balance',
        'office_initial_balance',
        'office_subsequent_balance',
        'executor',
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
        'initial_balance',
        'subsequent_balance',
        'holding_initial_balance',
        'holding_subsequent_balance',
        'company_initial_balance',
        'company_subsequent_balance',
        'office_initial_balance',
        'office_subsequent_balance',
        'executor',
        'operation_style',
        'quantity'
    ]