from salary.models import SalaryView
import datetime
import pandas as pd
from rest_framework.exceptions import ValidationError
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

        previous_month_salary_view = SalaryView.objects.filter(employee=employee, date=f"{previous_month.year}-{previous_month.month}-{1}").values('id', 'is_paid').last()
        
        try:
            if commission == True:
                salary_view = SalaryView.objects.get(employee=employee, date=f"{next_m.year}-{next_m.month}-{1}")
            else:
                if previous_month_salary_view is not None and previous_month_salary_view.is_paid == False:
                    salary_view = SalaryView.objects.get(employee=employee, date=f"{previous_month.year}-{previous_month.month}-{1}")
                else:
                    salary_view = SalaryView.objects.get(employee=employee, date=f"{now.year}-{now.month}-{1}")
        except:
            raise ValidationError({'detail': 'Ə/H cədvəli tapılmadı'})

        if func.__name__ == "advancepayment_create":
            if kwargs['amount'] is None:
                amount = (float(salary_view.final_salary) * 15) / 100
            else:
                amount = kwargs['amount']
        elif func.__name__ == "salary_pay_create":
            amount = float(salary_view.final_salary)
        else:
            amount = kwargs['amount']

        func(*args, **kwargs)

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
            else:
                salary_view.final_salary = salary_view.final_salary - float(amount)
        else:
            salary_view.final_salary = salary_view.final_salary + float(amount)

        salary_view.save()

    return wrapper