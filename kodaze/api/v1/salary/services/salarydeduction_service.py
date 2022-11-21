import datetime
from salary.models import SalaryView, SalaryDeduction
from rest_framework.exceptions import ValidationError
import pandas as pd
from api.v1.salary.decorators import add_amount_to_salary_view_decorator

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

