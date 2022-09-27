from django.contrib import admin
from .models import (
    HoldingCashboxIncome,
    HoldingCashboxExpense,
    OfficeCashboxIncome,
    OfficeCashboxExpense,
    CompanyCashboxIncome,
    CompanyCashboxExpense
) 
# Register your models here.
admin.site.register(HoldingCashboxIncome)
admin.site.register(HoldingCashboxExpense)
admin.site.register(OfficeCashboxIncome)
admin.site.register(OfficeCashboxExpense)
admin.site.register(CompanyCashboxIncome)
admin.site.register(CompanyCashboxExpense)
