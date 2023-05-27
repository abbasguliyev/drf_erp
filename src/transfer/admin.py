from django.contrib import admin
from .models import (
    HoldingTransfer,
    CompanyTransfer,
    OfficeTransfer
)

@admin.register(HoldingTransfer)
class HoldingTransferAdmin(admin.ModelAdmin):
    list_display = ("id", "sending_company", "receiving_company", "executor", "transfer_date", "transfer_amount", "recipient_subsequent_balance", "sender_subsequent_balance")
    list_display_links = ("id",)

@admin.register(CompanyTransfer)
class CompanyTransferAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "sending_office", "receiving_office", "executor", "transfer_date", "transfer_amount", "recipient_subsequent_balance", "sender_subsequent_balance")
    list_display_links = ("id", "company")

@admin.register(OfficeTransfer)
class OfficeTransferAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "sending_office", "receiving_office", "executor", "transfer_date", "transfer_amount", "recipient_subsequent_balance", "sender_subsequent_balance")
    list_display_links = ("id", "company")