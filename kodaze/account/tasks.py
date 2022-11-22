from salary.api.utils import create_fix_commission
from .models import User
import datetime
from holiday.models import EmployeeWorkingDay

from celery import shared_task
import pandas as pd
from salary.models import SalaryView
from company.models import PermissionForPosition
from salary.api.services import salary_view_service
from account.api.selectors import user_list

from salary.api.selectors import salary_view_list

@shared_task(name='salary_view_create_task')
def salary_view_create_task():
    """
    Periodik olaraq işçilərin maaş cədvəllərini create edən task. İşçi əlavə ediləndə aşağıdakı 
    create_employee_salary_view_task taskı işçi üçün maaş cədvəli create edir. Bu task isə
    növbəti aylarda periodik olaraq create etmək üçündür.
    """
    users = user_list()
    now = datetime.date.today()
    
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    for user in users:
        employee_salary_next_month = salary_view_list(filters={'employee':user, 'date__year': next_m.year, 'date__month': next_m.month}).count()
        if employee_salary_next_month != 0:
            continue
        else:
            salary_view_service.salary_view_create(employee=user, date=f"{next_m.year}-{next_m.month}-{1}", final_salary=user.salary)
            
    for user in users:
        
        employee_salary_this_month = salary_view_list(filters={'employee':user, 'date__year': now.year, 'date__month': now.month}).count()
        if employee_salary_this_month != 0:
            continue
        else:
            salary_view_service.salary_view_create(employee=user, date=f"{now.year}-{now.month}-{1}", final_salary=user.salary)

@shared_task(name='employee_fix_prim_auto_add')
def employee_fix_prim_auto_add():
    """
    İşçiyə fix komissiyaları verən task
    """
    create_fix_commission()


@shared_task(name='create_employee_salary_view_task')
def create_employee_salary_view_task(id):
    """
    İşçi register edildiyi zaman maaş cədvəlini create edən task
    """
    instance = user_list(filters={'id':id}).last()
    print(f"{instance=}")
    user = instance
    now = datetime.date.today()
    
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)
    
    employee_salary_this_month = salary_view_list(filters={'employee':user, 'date__year': now.year, 'date__month': now.month}).count()
    if employee_salary_this_month == 0:
        salary_view_service.salary_view_create(employee=user, date=f"{now.year}-{now.month}-{1}", final_salary=user.salary)

    employee_salary_next_month = salary_view_list(filters={'employee':user, 'date__year': next_m.year, 'date__month': next_m.month}).count()
    if employee_salary_next_month == 0:
        salary_view_service.salary_view_create(employee=user, date=f"{next_m.year}-{next_m.month}-{1}", final_salary=user.salary)


@shared_task(name='create_employee_working_day_task')
def create_employee_working_day_task(id):
    """
    İşçi register edildiyi zaman iş gününü create edən task
    """
    instance = user_list(filters={'id':id}).last()
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
    ).count()
    
    if employee_working_day_this_month == 0:
        employee_working_day = EmployeeWorkingDay.objects.create(
            employee=user,
            working_days_count=days_in_this_month,
            date=f"{now.year}-{now.month}-{1}"
        )
        employee_working_day.save()

    employee_working_day_next_month = EmployeeWorkingDay.objects.select_related('employee').filter(
        employee=user,
        date__year=next_m.year,
        date__month=next_m.month
    ).count()
    if employee_working_day_next_month == 0:
        employee_working_day = EmployeeWorkingDay.objects.create(
            employee=user,
            working_days_count=days_in_next_month,
            date=f"{next_m.year}-{next_m.month}-{1}"
        )
        employee_working_day.save()

@shared_task(name='create_user_permission_for_position_task')
def create_user_permission_for_position_task(id):
    """
    İşçi register edildiyi zaman ona verilmiş vəzifənin permissionları varsa, həmin permissionları 
    user-ə də əlavə edən task
    """
    instance = user_list(filters={'id':id}).last()
    user = instance
    user_position = instance.position
    positions = PermissionForPosition.objects.select_related('position', 'permission_group').filter(position=user_position)
    perm_list = set()
    for perm in positions:
        perm_list.add(perm.permission_group)
    print(f"{perm_list=}")
    user.groups.set(perm_list)
    user.save()