import datetime
from salary.models import Bonus
from rest_framework.exceptions import ValidationError
from salary.api.decorators import add_amount_to_salary_view_decorator
from salary.api.utils import salary_operation_delete
from salary.api.selectors import bonus_list

@add_amount_to_salary_view_decorator
def bonus_create(
        *, employee,
        amount: float = None,
        note: str = None,
        date: datetime.date = None,
        salary_date: datetime.date = None
) -> Bonus:
    """
    İşçilərə bonus vermək funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})

    if (amount == None):
        raise ValidationError({"detail": "Məbləği daxil edin"})
    
    bonus = Bonus.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date,
        salary_date=salary_date
    )

    bonus.full_clean()
    bonus.save()

    return bonus

def bonus_update(instance, **data):
    obj = bonus_list().filter(id=instance.id).update(**data)
    return obj

def bonus_delete(instance_list, func_name=None):
    for instance in instance_list:
        salary_operation_delete(instance=instance, func_name=func_name)