from celery import shared_task
import pandas as pd

import datetime
from .models import EmployeeWorkingDay
from account.api.selectors import user_list
from holiday.api.selectors import employee_working_day_list
from holiday.api.services.holiday_services import employee_working_day_create


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
           employee_working_day_create(employee=user, working_days_count=days_in_this_month, date=f"{now.year}-{now.month}-{1}")

    for user in users:
        employee_working_day_next_month = employee_working_day_list().filter(employee=user, date__month=next_m.month, date__year=next_m.year).count()
        if employee_working_day_next_month != 0:
            continue
        else:
            employee_working_day_create(employee=user, working_days_count=days_in_next_month, date=f"{next_m.year}-{next_m.month}-{1}")
    