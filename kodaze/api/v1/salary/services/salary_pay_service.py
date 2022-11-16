from datetime import date

from api.v1.cashbox.decorators import cashbox_expense_and_cash_flow_create
from salary.models import SalaryView, PaySalary
from rest_framework.exceptions import ValidationError
import pandas as pd

@cashbox_expense_and_cash_flow_create
def salary_pay_create(
        user,
        employee,
        note: str = None,
        date: date = None,
        salary_date: date = date.today()
) -> PaySalary:
    """
    İşçilərə maaş vermək funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})

    now = date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)

    total_payed_amount = 0

    salary_view = SalaryView.objects.get(employee=employee, date=f"{now.year}-{now.month}-{1}")

    if salary_view.is_done == True:
        raise ValidationError({"detail": "İşçinin maaşını artıq ödəmisiniz"})

    amount = salary_view.final_salary
    salary_view.final_salary = 0
    salary_view.is_done = True
    salary_view.pay_date = now
    salary_view.save()

    salary_pay = PaySalary.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date,
        salary_date=salary_date
    )

    salary_pay.full_clean()
    salary_pay.save()

    return salary_pay