from django.contrib import admin
from .models import (
    TransferFromHoldingToCompany,
    TransferFromOfficeToCompany,
    TransferFromCompanyToHolding,
    TransferFromCompanyToOffices
)
# Register your models here.
admin.site.register(TransferFromHoldingToCompany)
admin.site.register(TransferFromOfficeToCompany)
admin.site.register(TransferFromCompanyToHolding)
admin.site.register(TransferFromCompanyToOffices)