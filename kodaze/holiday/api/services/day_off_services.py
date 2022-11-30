import datetime
from rest_framework.exceptions import ValidationError
from holiday.models import (
    EmployeeDayOff,
    EmployeeDayOffHistory,
    EmployeeDayOffOperation
)
from holiday.api.selectors import employee_working_day_list, employee_day_off_history_list, employee_day_off_list, employee_day_off_operation_list
from account.api.selectors import user_list
from holiday.api.services.holiday_services import employee_working_day_decrease, employee_working_day_increase

def employee_day_off_create(
    *, employee,
    history,
    day_off_date: datetime.date.today(),
    is_paid: bool = False
) -> EmployeeDayOff:
    obj = EmployeeDayOff.objects.create(employee=employee, history=history, day_off_date=day_off_date, is_paid=is_paid)
    obj.full_clean()
    obj.save()

    return obj

def employee_day_off_history_create(
    *, note,
    is_paid: bool = False
) -> EmployeeDayOffHistory:
    obj = EmployeeDayOffHistory.objects.create(note=note, is_paid=is_paid)
    obj.full_clean()
    obj.save()

    return obj

def employee_day_off_operation_create(
    *, employee,
    day_off_date: str,
    is_paid: bool = False
) -> EmployeeDayOffOperation:
    day_off_date_list = day_off_date.split(',')
    for day_off_date in day_off_date_list:
        day_off_date_str = day_off_date.strip()
        h_d = datetime.datetime.strptime(day_off_date_str, '%d-%m-%Y')
        
        for emp in employee:
            emp_history = employee_day_off_history_list().filter(created_date=datetime.date.today(), is_paid=is_paid)
            if emp_history.count() == 0:
                history = employee_day_off_history_create(note=None, is_paid=is_paid)
            else:
                history = emp_history.last()
            
            emp_days_off = employee_day_off_list().filter(employee=emp, history=history, day_off_date=h_d, is_paid=is_paid)
            if emp_days_off.count != 0:
                continue

            employee_working_day_decrease(employee=emp, day_off_date=h_d)
            employee_day_off_create(employee=emp, history=history, day_off_date=h_d, is_paid=is_paid)
    obj = EmployeeDayOffOperation.objects.create(day_off_date=day_off_date, is_paid=is_paid)
    if employee is not None:
        obj.employee.set(employee)
    obj.full_clean()
    obj.save()

    return obj


def employee_day_off_history_delete(instance):
    emp_days_off = employee_day_off_list().filter(history=instance)
    for emp_day_off in emp_days_off:
        employee = emp_day_off.employee
        day_off_date = emp_day_off.day_off_date
        employee_working_day_increase(employee=employee, day_off_date=day_off_date)
    
    instance.delete()

def employe_paid_calculate(employee, working_day_count):
    salary = employee.salary
    amount = salary/working_day_count