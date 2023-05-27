from django.db.models.query import QuerySet
from contract.models import Contract, ContractGift, Installment, ContractCreditor, DemoSales


def contract_list(*, filters=None) -> QuerySet[Contract]:
    filters = filters or {}
    qs = Contract.objects.select_related(
        'group_leader', 
        'manager1', 
        'manager2', 
        'customer', 'customer__region', 
        'product', 
        'company', 
        'office',
        'old_contract'
    ).all()
    return qs

def contract_gift_list(*, filters=None) -> QuerySet[ContractGift]:
    filters = filters or {}
    qs = ContractGift.objects.select_related('product', 'contract').all()
    return qs


def installment_list(*, filters=None) -> QuerySet[Installment]:
    filters = filters or {}
    qs = Installment.objects.select_related('contract').all()
    return qs

def contract_creditor_list(*, filters=None) -> QuerySet[ContractCreditor]:
    filters = filters or {}
    qs = ContractCreditor.objects.select_related('contract', 'creditor').all()
    return qs

def demo_sales_list(*, filters=None) -> QuerySet[DemoSales]:
    filters = filters or {}
    qs = DemoSales.objects.select_related('user').all()
    return qs
