from django.db.models.query import QuerySet

from warehouse.models import (
    Warehouse
)

def warehouse_list(*, filters=None) -> QuerySet[Warehouse]:
    filters = filters or {}
    qs = Warehouse.objects.select_related('company', 'office').all()
    return qs
