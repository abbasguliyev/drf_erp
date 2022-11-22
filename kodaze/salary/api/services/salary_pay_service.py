import datetime
import pandas as pd
from cashbox.api.decorators import cashbox_operation_decorator
from salary.models import SalaryView, PaySalary
from rest_framework.exceptions import ValidationError
from salary.api.decorators import add_amount_to_salary_view_decorator
from enum import Enum
from cashbox import INCOME, EXPENSE
from salary.api.selectors import salary_view_list


@cashbox_operation_decorator
@add_amount_to_salary_view_decorator
def salary_pay_create(
        executor,
        employee,
        note: str = None,
        date: datetime.date = None,
        salary_date: datetime.date = None,
        operation = EXPENSE,
        func_name = None
) -> PaySalary:
    """
    İşçilərə maaş vermək funksiyası
    """

    if date is None:
        raise ValidationError({"detail": "Tarixi daxil edin"})

    now = datetime.date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    previous_month = d - pd.offsets.MonthBegin(1)
    
    previous_month_salary_view = salary_view_list(filters={'employee': employee, 'date': f"{previous_month.year}-{previous_month.month}-{1}"}).last()
    if previous_month_salary_view is not None and previous_month_salary_view.is_paid == False:
        salary_view = previous_month_salary_view
    else:
        salary_view = salary_view_list(filters={'employee': employee, 'date': f"{now.year}-{now.month}-{1}"}).last()

    if salary_view.is_paid == True:
        raise ValidationError({"detail": "İşçinin maaşını artıq ödəmisiniz"})

    amount = salary_view.final_salary
    
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