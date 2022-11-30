import datetime
from salary.models import SalaryDeduction
from rest_framework.exceptions import ValidationError
from salary.api.decorators import add_amount_to_salary_view_decorator
from salary.api.selectors import salary_deduction_list
from salary.api.utils import salary_operation_delete

@add_amount_to_salary_view_decorator
def salarydeduction_create(
        *, employee,
        amount: float = None,
        note: str = None,
        date: datetime.date = None,
        salary_date: datetime.date = None
) -> SalaryDeduction:
    """
    İşçinin maaşından kəsinti tutmaq funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})

    if (amount == None):
        raise ValidationError({"detail": "Məbləği daxil edin"})

    salary_deduction = SalaryDeduction.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date,
        salary_date=salary_date
    )

    salary_deduction.full_clean()
    salary_deduction.save()

    return salary_deduction

def salary_deduction_update(instance, **data):
    obj = salary_deduction_list().filter(id=instance.id).update(**data)
    return obj

def salary_deduction_delete(instance_list, func_name=None):
    for instance in instance_list:
        salary_operation_delete(instance=instance, func_name=func_name)