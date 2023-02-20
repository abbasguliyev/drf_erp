import datetime
import pandas as pd
from rest_framework.exceptions import ValidationError

from salary.api.selectors import (
    salary_view_list,
    employee_activity_history_list
)

from salary.api.services.employee_activity_service import employee_activity_history_create

from django.contrib.auth import get_user_model

User = get_user_model()

def add_amount_to_salary_view_decorator(func):
    def wrapper(*args, **kwargs):
        employee = kwargs['employee']

        try:
            func_name = kwargs['func_name']
        except:
            func_name = None

        if func.__name__ == "bonus_create":
            bonus = True
        else:
            bonus = False

        if func_name == "creditor_permission":
            creditor_commission = True
        else:
            creditor_commission = False

        try:
            date = kwargs['date']
        except:
            date = datetime.date.today()

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
                    next_month_salary_view = salary_view_list().filter(employee=employee, date=f"{next_m.year}-{next_m.month}-{1}").last()
                    if next_month_salary_view is not None:
                        salary_view = next_month_salary_view
                    else:
                        raise ValidationError({'detail': 'Xəta baş verdi'})
        except:
            raise ValidationError({'detail': 'Xəta baş verdi'})

        if func.__name__ == "advancepayment_create":
            if kwargs['amount'] is None:
                amount = (salary_view.final_salary * 30) / 100
            else:
                amount = kwargs['amount']
        elif func.__name__ == "salary_pay_create":
            amount = salary_view.final_salary
        else:
            amount = kwargs['amount']


        if creditor_commission == True:
            creditor = employee
            service_amount = amount
            creditor_permission = creditor.commission
            creditor_per_cent = creditor_permission.creditor_per_cent
            amount = (service_amount * int(creditor_per_cent)) / 100
            salary_view.final_salary = salary_view.final_salary + amount
        else:
            if bonus == False:
                if amount > salary_view.final_salary:
                    raise ValidationError({"detail": "Daxil edilmiş məbləği işçinin yekun maaşından çox ola bilməz"})
                
                salary_view.final_salary = salary_view.final_salary - amount
            else:
                salary_view.final_salary = salary_view.final_salary + amount

        salary_view.save()
        
        func(*args, **kwargs, salary_date=salary_view.date)

        employee_activity_history_create(
            salary_view = salary_view,
            func_name = func.__name__,
            amount = amount
        )

    return wrapper

def delete_emp_activity_history(func):
    def wrapper(*args, **kwargs): 
        func_name = kwargs['func_name']
        instance = kwargs['instance']
        employee = instance.employee
        date = instance.salary_date
        amount = instance.amount

        salary_view = salary_view_list().filter(employee=employee, date=f"{date.year}-{date.month}-{1}").last()
        history = employee_activity_history_list().filter(salary_view=salary_view).last()

        if func_name == 'advance_payment_delete':
            history.advance_payment = history.advance_payment - amount
            history.save()
            salary_view.final_salary = salary_view.final_salary + amount
            salary_view.save()
        if func_name == 'bonus_delete':
            history.bonus = history.bonus - amount
            history.save()
            salary_view.final_salary = salary_view.final_salary - amount
            salary_view.save()
        if func_name == 'salary_deduction_delete':
            history.salary_deduction = history.salary_deduction - amount
            history.save()
            salary_view.final_salary = salary_view.final_salary + amount
            salary_view.save()
        if func_name == 'salary_punishment_delete':
            history.salary_punishment = history.salary_punishment - amount
            history.save()
            salary_view.final_salary = salary_view.final_salary + amount
            salary_view.save()
        
        func(*args, **kwargs)

    return wrapper