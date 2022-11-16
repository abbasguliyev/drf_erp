from api.v1.cashbox.decorators import cashbox_expense_and_cash_flow_create
from datetime import date
from rest_framework.exceptions import ValidationError
import pandas as pd

from salary.models import AdvancePayment, SalaryView


@cashbox_expense_and_cash_flow_create
def advancepayment_create(
        user,
        employee,
        amount: float = None,
        note: str = None,
        date: date = None
) -> AdvancePayment:
    """
    İşçiyə avans vermə funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})
    
    if (amount == None):
        raise ValidationError({"detail": "Məbləği daxil edin"})

    now = date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)

    user_advanced_payment = AdvancePayment.objects.filter(employee=employee,
                                                          date=f"{date.year}-{date.month}-{1}").count()
    if user_advanced_payment > 2:
        raise ValidationError({"detail": "Bir işçiyə eyni ay ərzində maksimum 2 dəfə avans verilə bilər"})

    salary_view = SalaryView.objects.get(employee=employee, date=f"{now.year}-{now.month}-{1}")
    next_month_salary_view = SalaryView.objects.get(employee=employee, date=f"{date.year}-{date.month}-{1}")

    if amount is None:
        amount = (float(next_month_salary_view.final_salary) * 15) / 100
        
    if amount > salary_view.final_salary:
        raise ValidationError({"detail": "Daxil edilmiş məbləği işçinin yekun maaşından çox ola bilməz"})
    amount_after_advancedpayment = next_month_salary_view.final_salary - float(amount)

    salary_view.amount = amount
    next_month_salary_view.final_salary = amount_after_advancedpayment

    salary_view.save()
    next_month_salary_view.save()

    advance_payment = AdvancePayment.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date,
    )
    advance_payment.full_clean()
    advance_payment.save()

    return advance_payment
