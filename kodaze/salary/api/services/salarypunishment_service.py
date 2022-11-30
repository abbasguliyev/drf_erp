import datetime
from salary.models import SalaryPunishment
from rest_framework.exceptions import ValidationError
from salary.api.decorators import add_amount_to_salary_view_decorator
from salary.api.selectors import salary_punishment_list
from salary.api.utils import salary_operation_delete

@add_amount_to_salary_view_decorator
def salarypunishment_create(
        *, employee,
        amount: float = None,
        note: str = None,
        date: datetime.date = None,
        salary_date: datetime.date = None
) -> SalaryPunishment:
    """
    İşçinin maaşından cərimə tutmaq funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})

    if (amount == None):
        raise ValidationError({"detail": "Məbləği daxil edin"})

    salary_punishment = SalaryPunishment.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date,
        salary_date=salary_date
    )

    salary_punishment.full_clean()
    salary_punishment.save()

    return salary_punishment


def salary_punishment_update(instance, **data):
    obj = salary_punishment_list().filter(id=instance.id).update(**data)
    return obj

def salary_punishment_delete(instance_list_id, func_name=None):
    for instance in instance_list_id:
        salary_operation_delete(instance=instance, func_name=func_name)