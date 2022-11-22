from django.db.models.query import QuerySet
from cashbox.models import (
    HoldingCashbox,
    CompanyCashbox,
    OfficeCashbox,
    CashFlow,
    HoldingCashboxOperation,
    CompanyCashboxOperation
)

from cashbox.api.filters import (
    HoldingCashboxFilter,
    CompanyCashboxFilter,
    OfficeCashboxFilter,
    CashFlowFilter,
    HoldingCashboxOperationFilter,
    CompanyCashboxOperationFilter
)

def holding_cashbox_list(*, filters=None) -> QuerySet[HoldingCashbox]:
    filters = filters or {}
    qs = HoldingCashbox.objects.select_related('holding').all()
    return HoldingCashboxFilter(filters, qs).qs

def company_cashbox_list(*, filters=None) -> QuerySet[CompanyCashbox]:
    filters = filters or {}
    qs = CompanyCashbox.objects.select_related('company').all()
    return CompanyCashboxFilter(filters, qs).qs

def office_cashbox_list(*, filters=None) -> QuerySet[OfficeCashbox]:
    filters = filters or {}
    qs = OfficeCashbox.objects.select_related('office').all()
    return OfficeCashboxFilter(filters, qs).qs

def cash_flow_list(*, filters=None) -> QuerySet[CashFlow]:
    filters = filters or {}
    qs = CashFlow.objects.select_related(
        'holding', 'company', 'office', 'executor', 'customer', 'personal'
    ).all()
    return CashFlowFilter(filters, qs).qs

def holding_cashbox_opr_list(*, filters=None) -> QuerySet[HoldingCashboxOperation]:
    filters = filters or {}
    qs = HoldingCashboxOperation.objects.select_related('executor', 'personal').all()
    return HoldingCashboxOperationFilter(filters, qs).qs

def company_cashbox_opr_list(*, filters=None) -> QuerySet[CompanyCashboxOperation]:
    filters = filters or {}
    qs = CompanyCashboxOperation.objects.select_related('executor', 'personal', 'company', 'office').all()
    return CompanyCashboxOperationFilter(filters, qs).qs
