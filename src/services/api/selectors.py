from services.models import Service, ServicePayment, ServiceProductForContract
from django.db.models.query import QuerySet

def service_list(*, filters=None) -> QuerySet[Service]:
    filters = filters or {}
    qs = Service.objects.select_related('customer', 'contract', 'service_creditor', 'operator').prefetch_related('product').all()
    return qs

def service_payment_list(*, filters=None) -> QuerySet[ServicePayment]:
    filters = filters or {}
    qs = ServicePayment.objects.select_related('service').all()
    return qs

def service_product_for_contract_list(*, filters=None) -> QuerySet[ServiceProductForContract]:
    filters = filters or {}
    qs = ServiceProductForContract.objects.select_related('company', 'product').all()
    return qs
