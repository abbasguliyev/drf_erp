from warehouse.models import Warehouse
from warehouse.api.selectors import warehouse_list

def warehouse_create(
    *, name: str, 
    office,
    company = None
) -> Warehouse:
    obj = Warehouse.objects.create(name=name, office=office, company=office.company)
    obj.full_clean()
    obj.save()

    return obj

def warehouse_update(instance, data) -> Warehouse:
    obj = warehouse_list().filter(pk=instance.id).update(**data)
    obj.save()

    return obj

def warehouse_delete(instance):
    instance.is_active = False
    instance.save()