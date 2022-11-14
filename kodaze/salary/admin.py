from django.contrib import admin
from .models import (
    AdvancePayment, 
    Bonus, 
    SalaryDeduction,
    SalaryView,
    PaySalary,
    SaleRange,
    MonthRange,
    CommissionSaleRange,
    CommissionInstallment,
    Commission
)
# Register your models here.

@admin.register(SalaryView)
class SalaryViewAdmin(admin.ModelAdmin):
    search_fields = (
        "employee__id",
        "employee__fullname",
        
    )
    list_filter = [
        "employee__id",
        "date"
    ]
    list_display = (
        "id",
        "employee",
        "date",
        "sale_quantity",
        "sales_amount",
        "final_salary",
        "is_done",
        "amount",
        "note",
    )

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'commission_name', 'for_office', 'cash', 'for_team')
    search_fields = ('commission_name',)
    list_filter = ('commission_name',)

@admin.register(SaleRange)
class SaleRangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_count', 'end_count')

@admin.register(MonthRange)
class MonthRangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_month', 'end_month')

@admin.register(CommissionSaleRange)
class CommissionSaleRangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale_range', 'amount', 'sale_type')

@admin.register(CommissionInstallment)
class CommissionInstallmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'month_range', 'amount')

@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'amount', 'date')
    
admin.site.register(AdvancePayment)
admin.site.register(SalaryDeduction)
admin.site.register(PaySalary)
