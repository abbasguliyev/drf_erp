import datetime
import pandas as pd
from rest_framework.exceptions import ValidationError

from salary.api.selectors import (
    salary_view_list
)

from salary.api.services.employee_activity_service import employee_activity_history_create

from django.contrib.auth import get_user_model

User = get_user_model()

def add_amount_to_salary_view_decorator(func):
    def wrapper(*args, **kwargs):
        employee = kwargs['employee']

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

        previous_month_salary_view = salary_view_list().filter(employee=employee, date=f"{previous_month.year}-{previous_month.month}-{1}").last()
        
        try:
            if previous_month_salary_view is not None and previous_month_salary_view.is_paid == False:
                salary_view = previous_month_salary_view
            else:
                current_salary_view = salary_view_list().filter(employee=employee, date=f"{now.year}-{now.month}-{1}").last()
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


        if bonus == False:
            if float(amount) > salary_view.final_salary:
                raise ValidationError({"detail": "Daxil edilmiş məbləği işçinin yekun maaşından çox ola bilməz"})
            
            salary_view.final_salary = salary_view.final_salary - float(amount)
        else:
            salary_view.final_salary = salary_view.final_salary + float(amount)

        salary_view.save()
        
        func(*args, **kwargs, salary_date=salary_view.date)

        employee_activity_history_create(
            salary_view = salary_view,
            func_name = func.__name__,
            amount = amount
        )

    return wrapper
