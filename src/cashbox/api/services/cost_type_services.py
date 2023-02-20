from cashbox.api.selectors import cost_type_list
from cashbox.models import CostType

def create_cost_type(*, name: str) -> CostType:
    obj = CostType.objects.create(name=name)
    obj.full_clean()
    obj.save()

    return obj

def update_cost_type(instance, **data) -> CostType:
    obj = cost_type_list().filter(pk=instance.pk).update(**data)
    return obj
