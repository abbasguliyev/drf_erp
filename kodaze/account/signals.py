from salary.models import SalaryView
from account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import pandas as pd
from holiday.models import EmployeeWorkingDay

@receiver(post_save, sender=User)
def create_employee_salary_view(sender, instance, created, **kwargs):
    if created:
        user = instance
        now = datetime.date.today()
        
        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)
        
        employee_salary_this_month = SalaryView.objects.select_related('employee').filter(
            employee=user,
            date__year=now.year,
            date__month=now.month
        )
        if len(employee_salary_this_month) == 0:
            SalaryView.objects.create(
                employee=user, date=f"{now.year}-{now.month}-{1}", final_salary=user.salary).save()

        employee_salary_novbeti_ay = SalaryView.objects.select_related('employee').filter(
            employee=user,
            date__year=next_m.year,
            date__month=next_m.month
        )
        if len(employee_salary_novbeti_ay) == 0:
            SalaryView.objects.create(
                employee=user, date=f"{next_m.year}-{next_m.month}-{1}", final_salary=user.salary).save()


@receiver(post_save, sender=User)
def create_employee_working_day(sender, instance, created, **kwargs):
    if created:
        user = instance
        now = datetime.date.today()

        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

        next_m = d + pd.offsets.MonthBegin(1)

        days_in_this_month = pd.Period(
            f"{now.year}-{now.month}-{1}").days_in_month

        days_in_next_month = pd.Period(
            f"{next_m.year}-{next_m.month}-{1}").days_in_month

        employee_working_day_this_month = EmployeeWorkingDay.objects.select_related('employee').filter(
            employee=user,
            date__year=now.year,
            date__month=now.month
        )
        
        if len(employee_working_day_this_month) == 0:
            employee_working_day = EmployeeWorkingDay.objects.create(
                employee=user,
                working_days_count=days_in_this_month,
                date=f"{now.year}-{now.month}-{1}"
            )
            employee_working_day.save()

        employee_working_day = EmployeeWorkingDay.objects.select_related('employee').filter(
            employee=user,
            date__year=next_m.year,
            date__month=next_m.month
        )
        if len(employee_working_day) == 0:
            employee_working_day = EmployeeWorkingDay.objects.create(
                employee=user,
                working_days_count=days_in_next_month,
                date=f"{next_m.year}-{next_m.month}-{1}"
            )
            employee_working_day.save()