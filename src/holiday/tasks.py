from celery import shared_task
import pandas as pd
import math

import datetime
from account.api.selectors import user_list
from holiday.api.selectors import employee_working_day_list

from holiday.api.services import holiday_services, day_off_services
from holiday.api.selectors import (
    employee_holiday_history_list, 
    employee_working_day_list, 
    employee_day_off_history_list
)
from account import FIX, FIX_COMISSION


@shared_task(name='employee_working_day_creater_task')
def employee_working_day_creater_task():
    """
    Periodik olaraq iş gününü create edən task
    """
    now = datetime.date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)
    days_in_this_month = pd.Period(f"{now.year}-{now.month}-{1}").days_in_month
    days_in_next_month = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    users = user_list()

    for user in users:
        employee_working_day_this_month = employee_working_day_list().filter(employee=user, date__month=now.month, date__year=now.year).count()
        if employee_working_day_this_month != 0:
            continue
        else:
           holiday_services.employee_working_day_create(employee=user, working_days_count=days_in_this_month, date=f"{now.year}-{now.month}-{1}")

    for user in users:
        employee_working_day_next_month = employee_working_day_list().filter(employee=user, date__month=next_m.month, date__year=next_m.year).count()
        if employee_working_day_next_month != 0:
            continue
        else:
            holiday_services.employee_working_day_create(employee=user, working_days_count=days_in_next_month, date=f"{next_m.year}-{next_m.month}-{1}")
    

@shared_task(name='holiday_operation_create_task')
def holiday_operation_create_task(holiday_date_list, employee_list, person_on_duty_list=None):
    """
    Tətil əlavə etmə prosesini yerinə yetirən task
    """
    person_on_duty = []
    for holiday_date in holiday_date_list:
        holiday_date_str = holiday_date.strip()
        h_d = datetime.datetime.strptime(holiday_date_str, '%d-%m-%Y')
        
        for employee_id in employee_list:
            employee = user_list().filter(pk=employee_id).order_by('pk').last()
            for person_on_duty_id in person_on_duty_list:
                emp = user_list().filter(pk=person_on_duty_id).order_by('pk').last()
                person_on_duty.append(emp)
            if employee in person_on_duty:
                continue
            
            emp_history = employee_holiday_history_list().filter(employee=employee, created_date=datetime.date.today())
            if emp_history.count() == 0:
                history = holiday_services.employee_holiday_history_create(employee=employee, note=None)
            else:
                history = emp_history.last()
            
            holiday_services.employee_working_day_decrease(employee=employee, holiday_date=h_d)
            holiday_services.employee_holiday_create(employee=employee, history=history, holiday_date=h_d)

@shared_task(name='employee_day_off_operation_create_task')
def employee_day_off_operation_create_task(day_off_date_list, employee_list, is_paid):
    """
    İcazə əlavə etmə prosesini yerinə yetirən task
    """
    for day_off_date in day_off_date_list:
        day_off_date_str = day_off_date.strip()
        h_d = datetime.datetime.strptime(day_off_date_str, '%d-%m-%Y')
        for employee_id in employee_list:
            employee = user_list().filter(pk=employee_id).order_by('pk').last()
            emp_history = employee_day_off_history_list().filter(employee=employee, created_date=datetime.date.today(), is_paid=is_paid)
            if emp_history.count() == 0:
                history = day_off_services.employee_day_off_history_create(employee=employee, note=None, is_paid=is_paid)
            else:
                history = emp_history.last()
            
            working_day_count = holiday_services.employee_working_day_decrease(employee=employee, holiday_date=h_d)
            if is_paid == False:
                if employee.salary_style == FIX_COMISSION or employee.salary_style == FIX:
                    paid_amount = day_off_services.employe_unpaid_day_off(employee=employee, working_day_count=working_day_count)
                else:
                    paid_amount = 0
            else:
                paid_amount = 0
            # paid_amount = "%.2f" % paid_amount
            paid_amount = math.ceil(paid_amount)
            day_off_services.employee_day_off_create(employee=employee, history=history, day_off_date=h_d, is_paid=is_paid, paid_amount=paid_amount)
