import datetime
from salary.models import SalaryPunishment, SalaryView
from rest_framework.exceptions import ValidationError
import pandas as pd
from api.v1.salary.decorators import add_amount_to_salary_view_decorator

@add_amount_to_salary_view_decorator
def salarypunishment_create(
        *, employee,
        amount: float = None,
        note: str = None,
        date: datetime.date = None
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
        date=date
    )

    salary_punishment.full_clean()
    salary_punishment.save()

    return salary_punishment

