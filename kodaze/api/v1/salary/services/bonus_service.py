from datetime import date
from salary.models import SalaryView, Bonus
from rest_framework.exceptions import ValidationError
import pandas as pd

def bonus_create(
        *, employee,
        amount: float = None,
        note: str = None,
        date: date = None
) -> Bonus:
    """
    İşçilərə bonus vermək funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})

    if (amount == None):
        raise ValidationError({"detail": "Məbləği daxil edin"})

    now = date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)
    
    salary_view = SalaryView.objects.get(employee=employee, date=next_m)
    salary_view.final_salary = salary_view.final_salary + float(amount)

    salary_view.save()

    bonus = Bonus.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date
    )

    bonus.full_clean()
    bonus.save()

    return bonus