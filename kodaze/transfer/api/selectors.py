from django.db.models.query import QuerySet

from transfer.models import (
    HoldingTransfer,
    CompanyTransfer,
    OfficeTransfer,
)

from transfer.api.filters import (
    HoldingTransferFilter,
    CompanyTransferFilter,
    OfficeTransferFilter,
)

def holding_transfer_list(*, filters=None) -> QuerySet[HoldingTransfer]:
    filters = filters or {}
    qs = HoldingTransfer.objects.select_related('executor', 'sending_company', 'receiving_company').all()
    return HoldingTransferFilter(filters, qs).qs

def company_transfer_list(*, filters=None) -> QuerySet[CompanyTransfer]:
    filters = filters or {}
    qs = CompanyTransfer.objects.select_related('executor', 'company', 'sending_office', 'receiving_office').all()
    return CompanyTransferFilter(filters, qs).qs

def office_transfer_list(*, filters=None) -> QuerySet[OfficeTransfer]:
    filters = filters or {}
    qs = OfficeTransfer.objects.select_related('executor', 'company', 'sending_office', 'receiving_office').all()
    return OfficeTransferFilter(filters, qs).qs
