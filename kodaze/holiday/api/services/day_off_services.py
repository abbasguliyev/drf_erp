import datetime
import pandas as pd
from rest_framework.exceptions import ValidationError
from holiday.models import (
    EmployeeDayOff,
    EmployeeDayOffHistory,
    EmployeeDayOffOperation
)
from account import FIX, FIX_COMISSION
from holiday.api.selectors import employee_day_off_history_list, employee_day_off_list, employee_day_off_operation_list
from holiday.api.services.holiday_services import employee_working_day_decrease, employee_working_day_increase
from salary.api.decorators import add_amount_to_salary_view_decorator

from salary.api.decorators import delete_emp_activity_history
from salary.api.selectors import salary_view_list


def employee_day_off_create(
    *, employee,
    history,
    day_off_date: datetime.date.today(),
    is_paid: bool = False,
    paid_amount: float = 0
) -> EmployeeDayOff:
    obj = EmployeeDayOff.objects.create(employee=employee, history=history, day_off_date=day_off_date, is_paid=is_paid, paid_amount=paid_amount)
    obj.full_clean()
    obj.save()

    return obj

def employee_day_off_history_create(
    *, employee,  
    note,
    is_paid: bool = False
) -> EmployeeDayOffHistory:
    obj = EmployeeDayOffHistory.objects.create(employee=employee, note=note, is_paid=is_paid)
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
            emp_history = employee_day_off_history_list().filter(employee=emp, created_date=datetime.date.today(), is_paid=is_paid)
            if emp_history.count() == 0:
                history = employee_day_off_history_create(employee=emp, note=None, is_paid=is_paid)
            else:
                history = emp_history.last()
            
            emp_days_off = employee_day_off_list().filter(employee=emp, history=history, day_off_date=h_d, is_paid=is_paid)
            if emp_days_off.count() != 0:
                continue
            working_day_count = employee_working_day_decrease(employee=emp, holiday_date=h_d)
            if is_paid == True:
                if emp.salary_style == FIX_COMISSION or emp.salary_style == FIX:
                    paid_amount = employe_paid_day_off(employee=emp, working_day_count=working_day_count)
                else:
                    paid_amount = 0
            else:
                paid_amount = 0

            employee_day_off_create(employee=emp, history=history, day_off_date=h_d, is_paid=is_paid, paid_amount=paid_amount)
    obj = EmployeeDayOffOperation.objects.create(day_off_date=day_off_date, is_paid=is_paid)
    if employee is not None:
        obj.employee.set(employee)
    obj.full_clean()
    obj.save()

    return obj

def employe_paid_day_off(employee, working_day_count):
    """
    Ödənişli icazə günü verildikdə işçinin yekun maaşından məbləğ çıxan funksiya
    """
    now = datetime.date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
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
    
    salary = employee.salary
    amount = salary/working_day_count
    salary_view.final_salary = salary_view.final_salary - amount
    salary_view.save()

    return amount

def employe_get_back_paid_amount_day_off(instance):
    """
    Ödənişli icazə günü silindikdə işçinin yekun maaşına məbləğ qaytaran funksiya
    """
    employee = instance.employee
    paid_amount = instance.paid_amount
    now = datetime.date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
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
    
    salary_view.final_salary = salary_view.final_salary + paid_amount
    salary_view.save()

    return paid_amount


def employee_day_off_history_update(instance, **data):
    obj = employee_day_off_history_list().filter(id=instance.id).update(**data)
    return obj

def employee_day_off_history_delete(instance):
    emp_days_off = employee_day_off_list().filter(history=instance)
    for emp_day_off in emp_days_off:
        employee = emp_day_off.employee
        day_off_date = emp_day_off.day_off_date
        employee_working_day_increase(employee=employee, holiday_date=day_off_date)
        employe_get_back_paid_amount_day_off(instance=emp_day_off)
    instance.delete()

def days_off_history_delete_service(instance_list):
    for instance in instance_list:
        employee_day_off_history_delete(instance=instance)
