from django.db.models.query import QuerySet
from cashbox.models import (
    HoldingCashbox,
    CompanyCashbox,
    OfficeCashbox,
    CashFlow,
    HoldingCashboxOperation,
    CompanyCashboxOperation,
    CostType
)

def holding_cashbox_list(*, filters=None) -> QuerySet[HoldingCashbox]:
    filters = filters or {}
    qs = HoldingCashbox.objects.select_related('holding').all()
    return qs

def company_cashbox_list(*, filters=None) -> QuerySet[CompanyCashbox]:
    filters = filters or {}
    qs = CompanyCashbox.objects.select_related('company').all()
    return qs

def office_cashbox_list(*, filters=None) -> QuerySet[OfficeCashbox]:
    filters = filters or {}
    qs = OfficeCashbox.objects.select_related('office').all()
    return qs

def cash_flow_list(*, filters=None) -> QuerySet[CashFlow]:
    filters = filters or {}
    qs = CashFlow.objects.select_related(
        'holding', 'company', 'office', 'executor', 'customer', 'personal'
    ).all()
    return qs

def holding_cashbox_opr_list(*, filters=None) -> QuerySet[HoldingCashboxOperation]:
    filters = filters or {}
    qs = HoldingCashboxOperation.objects.select_related('executor', 'personal').all()
    return qs

def company_cashbox_opr_list(*, filters=None) -> QuerySet[CompanyCashboxOperation]:
    filters = filters or {}
    qs = CompanyCashboxOperation.objects.select_related('executor', 'personal', 'company', 'office').all()
    return qs

def cost_type_list(*, filters=None) -> QuerySet[CostType]:
    filters = filters or {}
    qs = CostType.objects.all()
    return qs
