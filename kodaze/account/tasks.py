import datetime
from company.models import Position
from .models import User
import datetime
import pandas as pd
from holiday.models import EmployeeWorkingDay

from celery import shared_task, app
import pandas as pd
from salary.models import Manager2Prim, SalaryView, OfficeLeaderPrim, GroupLeaderPrimNew



@shared_task(name='salary_view_create_task')
def salary_view_create_task():
    users = User.objects.all()
    now = datetime.date.today()
    
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    for user in users:
        employee_salary = SalaryView.objects.select_related('employee').filter(
            employee=user, 
            date__year = next_m.year,
            date__month = next_m.month
        )
        if len(employee_salary) != 0:
            continue
        else:
            SalaryView.objects.create(employee=user, date=f"{next_m.year}-{next_m.month}-{1}", final_salary=user.salary).save()
            
    for user in users:
        employee_salary = SalaryView.objects.select_related('employee').filter(
            employee=user, 
            date__year = now.year,
            date__month = now.month
        )
        if len(employee_salary) != 0:
            continue
        else:
            SalaryView.objects.create(employee=user, date=f"{now.year}-{now.month}-{1}", final_salary=user.salary).save()

@shared_task(name='employee_fix_prim_auto_add')
def employee_fix_prim_auto_add():
    now = datetime.date.today()

    this_month = f"{now.year}-{now.month}-{1}"
    
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    previus_month = d - pd.offsets.MonthBegin(1)

    officeLeaderPosition = Position.objects.filter(name="OFFICE LEADER")[0]
    officeLeaders = User.objects.filter(position__name=officeLeaderPosition.name)

    for officeLeader in officeLeaders:
        officeLeader_status = officeLeader.employee_status

        officeleader_prim = OfficeLeaderPrim.objects.get(prim_status=officeLeader_status, position=officeLeader.position)
        officeLeader_salary_view_this_month = SalaryView.objects.get(employee=officeLeader, date=this_month)

        officeLeader_salary_view_this_month.final_salary = float(officeLeader_salary_view_this_month.final_salary) + float(officeleader_prim.fix_prim)
        officeLeader_salary_view_this_month.save()

    manager2Position = Position.objects.filter(name="CANVASSER")[0]
    manager2s = User.objects.filter(position__name=manager2Position.name)

    for manager2 in manager2s:
        manager2_status = manager2.employee_status

        manager2_prim = Manager2Prim.objects.get(prim_status=manager2_status, position=manager2.position)

        manager2_salary_view_previus_month = SalaryView.objects.get(employee=manager2, date=previus_month)
        manager2_salary_goruntulenme_this_month = SalaryView.objects.get(employee=manager2, date=f"{now.year}-{now.month}-{1}")

        prim_for_sales_quantity = 0
        if (manager2_salary_view_previus_month.sale_quantity == 0):
            prim_for_sales_quantity = manager2_prim.sale0
        elif (manager2_salary_view_previus_month.sale_quantity >= 1) and (manager2_salary_view_previus_month.sale_quantity <= 8):
            prim_for_sales_quantity = manager2_prim.sale1_8

        manager2_salary_goruntulenme_this_month.final_salary = float(manager2_salary_goruntulenme_this_month.final_salary) + float(prim_for_sales_quantity) + float(manager2_prim.fix_prim)
        manager2_salary_goruntulenme_this_month.save()
        manager2_salary_view_previus_month.save()

@shared_task(name='create_employee_salary_view_task')
def create_employee_salary_view_task(id):
    instance = User.objects.select_related(
                'company', 'office', 'section', 'position', 'team', 'employee_status'
            ).get(id=id)
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


@shared_task(name='create_employee_working_day_task')
def create_employee_working_day_task(id):
    instance = User.objects.select_related(
            'company', 'office', 'section', 'position', 'team', 'employee_status'
        ).get(id=id)
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