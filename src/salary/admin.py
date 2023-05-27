from django.contrib import admin
from .models import (
    AdvancePayment, 
    Bonus, 
    SalaryDeduction,
    SalaryPunishment,
    SalaryView,
    PaySalary,
    SaleRange,
    MonthRange,
    CommissionSaleRange,
    CommissionInstallment,
    Commission,
    SalaryViewExport,
    EmployeeActivityHistory
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
        "commission_amount",
        "final_salary",
        "is_done",
        "amount",
        "note",
    )

class SalaryOprAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'amount', 'date', 'salary_date', 'is_paid')
    list_filter = [
        "employee",
        "date", 
        'salary_date',
        'is_paid'
    ]

    class Meta:
        abstract = True

@admin.register(SalaryViewExport)
class SalaryViewExportAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_data', 'export_date')
    
@admin.register(AdvancePayment)
class AdvancePaymentAdmin(SalaryOprAdmin):
    pass

@admin.register(SalaryDeduction)
class SalaryDeductionAdmin(SalaryOprAdmin):
    pass

@admin.register(SalaryPunishment)
class SalaryPunishmentAdmin(SalaryOprAdmin):
    pass

@admin.register(Bonus)
class BonusAdmin(SalaryOprAdmin):
    pass

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

@admin.register(EmployeeActivityHistory)
class EmployeeActivityHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'salary_view', 'bonus', 'advance_payment', 'salary_deduction', 'salary_punishment', 'activity_date')
    list_filter = ('salary_view',)
    list_display_links = ('id', 'salary_view')

admin.site.register(PaySalary)
