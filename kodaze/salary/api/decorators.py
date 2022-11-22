from salary.models import SalaryView, AdvancePayment, Bonus, SalaryDeduction, SalaryPunishment
import datetime
import pandas as pd
from rest_framework.exceptions import ValidationError

from salary.api.selectors import (
    advance_payment_list,
    salary_deduction_list,
    salary_punishment_list,
    bonus_list,
    pay_salary_list,
    salary_view_list
)

from django.contrib.auth import get_user_model

User = get_user_model()

def add_amount_to_salary_view_decorator(func):
    def wrapper(*args, **kwargs):
        employee = kwargs['employee']
        try:
            commission = kwargs['comission']
        except:
            commission = False

        if func.__name__ == "bonus_create":
            bonus = True
        else:
            bonus = False

        date = kwargs['date']
        if date == None:
            date = datetime.date.today()

        now = datetime.date.today()
        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)
        previous_month = d - pd.offsets.MonthBegin(1)

        previous_month_salary_view = salary_view_list(filters={'employee': employee, 'date': f"{previous_month.year}-{previous_month.month}-{1}"}).last()
        
        try:
            if commission == True:
                salary_view = salary_view_list(filters={'employee': employee, 'date': f"{next_m.year}-{next_m.month}-{1}"}).last()
            else:
                if previous_month_salary_view is not None and previous_month_salary_view.is_paid == False:
                    salary_view = previous_month_salary_view
                else:
                    current_salary_view = salary_view_list(filters={'employee': employee, 'date': f"{now.year}-{now.month}-{1}"}).last()
                    if current_salary_view.is_paid == False:
                        salary_view = current_salary_view
                    else:
                        raise ValidationError({'detail': 'Ə/H artıq ödənilib'})
        except ValidationError as err:
            raise err

        if func.__name__ == "advancepayment_create":
            if kwargs['amount'] is None:
                amount = (float(salary_view.final_salary) * 15) / 100
            else:
                amount = kwargs['amount']
        elif func.__name__ == "salary_pay_create":
            amount = float(salary_view.final_salary)
        else:
            amount = kwargs['amount']

        func(*args, **kwargs, salary_date=salary_view.date)

        if bonus == False:
            if float(amount) > salary_view.final_salary:
                raise ValidationError({"detail": "Daxil edilmiş məbləği işçinin yekun maaşından çox ola bilməz"})
            
            if func.__name__ == "salary_pay_create":
                amount = float(salary_view.final_salary)
                salary_view.final_salary = 0
                salary_view.is_done = True
                salary_view.is_paid = True
                salary_view.pay_date = now
                salary_view.save()

                all_bonus = bonus_list(filters={'employee': employee, 'salary_date__month': salary_view.date.month, 'salary_date__year': salary_view.date.year}) 
                all_sd = salary_deduction_list(filters={'employee': employee, 'salary_date__month': salary_view.date.month, 'salary_date__year': salary_view.date.year}).filter()
                all_sp = salary_punishment_list(filters={'employee': employee, 'salary_date__month': salary_view.date.month, 'salary_date__year': salary_view.date.year})

                for b in all_bonus:
                    b.is_paid = True
                    b.save()
                for sd in all_sd:
                    sd.is_paid = True
                    sd.save()
                for sp in all_sp:
                    sp.is_paid = True
                    sp.save()
            else:
                salary_view.final_salary = salary_view.final_salary - float(amount)
        else:
            salary_view.final_salary = salary_view.final_salary + float(amount)

        salary_view.save()

    return wrapper