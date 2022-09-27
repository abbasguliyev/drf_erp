from django.contrib import admin
from cashbox.models import (
    OfficeCashbox,
    CompanyCashbox,
    HoldingCashbox,
    CashFlow
)
# Register your models here.
admin.site.register(OfficeCashbox)
admin.site.register(CompanyCashbox)
admin.site.register(HoldingCashbox)
admin.site.register(CashFlow)
