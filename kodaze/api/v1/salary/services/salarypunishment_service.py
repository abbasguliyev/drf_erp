from datetime import date
from salary.models import SalaryPunishment, SalaryView
from rest_framework.exceptions import ValidationError
import pandas as pd


def salarypunishment_create(
        *, employee,
        amount: float = None,
        note: str = None,
        date: date = None
) -> SalaryPunishment:
    """
    İşçinin maaşından cərimə tutmaq funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})

    if (amount == None):
        raise ValidationError({"detail": "Məbləği daxil edin"})

    now = date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)

    salary_view = SalaryView.objects.get(employee=employee, date=next_m)
    salary_view.final_salary = salary_view.final_salary - float(amount)

    salary_view.save()

    salary_punishment = SalaryPunishment.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date
    )

    salary_punishment.full_clean()
    salary_punishment.save()

    return salary_punishment

