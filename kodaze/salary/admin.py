from django.contrib import admin
from .models import (
    AdvancePayment, 
    Bonus, 
    Manager2Prim, 
    Manager1PrimNew, 
    SalaryDeduction, 
    SalaryView,
    GroupLeaderPrimNew, 
    PaySalary, 
    CreditorPrim, 
    OfficeLeaderPrim
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

admin.site.register(AdvancePayment)
admin.site.register(Bonus)
admin.site.register(Manager2Prim)
admin.site.register(Manager1PrimNew)
admin.site.register(SalaryDeduction)
admin.site.register(GroupLeaderPrimNew)
admin.site.register(PaySalary)
admin.site.register(CreditorPrim)
admin.site.register(OfficeLeaderPrim)

