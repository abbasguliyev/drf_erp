import datetime
from rest_framework.exceptions import ValidationError
from holiday.models import (
    EmployeeWorkingDay,
    EmployeeHoliday,
    EmployeeHolidayHistory,
    HolidayOperation
)
from holiday.api.selectors import employee_holiday_history_list, employee_working_day_list, employee_holiday_list, employee_day_off_list
from account.api.selectors import user_list
from account import HOLDING, COMPANY
from holiday.tasks import holiday_operation_create_task

from django.db import transaction
import numpy as np

def employee_working_day_create(
    *, employee,
    working_days_count,
    date: datetime.date.today()
) -> EmployeeWorkingDay:
    obj = EmployeeWorkingDay.objects.create(employee=employee, working_days_count=working_days_count, date=date)
    obj.full_clean()
    obj.save()

    return obj

def employee_working_day_increase(employee, holiday_date) -> int:
    emp_working_day = employee_working_day_list().filter(employee=employee, date__month=holiday_date.month, date__year=holiday_date.year).last()
    emp_working_day.working_days_count += 1
    emp_working_day.save()

    return emp_working_day.working_days_count

def employee_working_day_decrease(employee, holiday_date) -> int:
    emp_working_day = employee_working_day_list().filter(employee=employee, date__month=holiday_date.month, date__year=holiday_date.year).last()
    emp_working_day.working_days_count -= 1
    emp_working_day.save()
    return emp_working_day.working_days_count

def employee_holiday_create(
    *, employee,
    history,
    holiday_date: datetime.date.today()
) -> EmployeeHoliday:
    obj = EmployeeHoliday.objects.create(employee=employee, history=history, holiday_date=holiday_date)
    obj.full_clean()
    obj.save()

    return obj

def employee_holiday_history_create(employee, note: str = None) -> EmployeeHolidayHistory:
    obj = EmployeeHolidayHistory.objects.create(employee=employee, note=note)
    obj.full_clean()
    obj.save()

    return obj

def holiday_operation_create(
    *, holiday_date: str,
    holding: bool = False,
    company = None,
    office = None,
    person_on_duty = None
) -> HolidayOperation:
    holiday_date_list = holiday_date.split(',')
    employees = None
    if holding is True:
        employees_count = user_list().filter(register_type=HOLDING).count()
        if employees_count == 0:
            raise ValidationError({"detail": "Holdinqə aid işçi tapılmadı."})
        else:
            employees = user_list().filter(register_type=HOLDING)
    else:
        employees_count = user_list().filter(register_type=COMPANY, office=office).count()
        if employees_count == 0:
            raise ValidationError({"detail": "Bu ofisə bağlı işçi tapılmadı"})
        else:
            employees = user_list().filter(register_type=COMPANY, office=office)
        if office.company != company:
            raise ValidationError({"detail": "Ofis Şirkətə məxsus deyil"})

    for holiday_date in np.array(holiday_date_list):
        holiday_date_str = holiday_date.strip()
        h_d = datetime.datetime.strptime(holiday_date_str, '%d-%m-%Y')
        
        for employee in employees.iterator():
            if employee in np.array(person_on_duty):
                continue
            
            emp_days_off = employee_day_off_list().filter(employee=employee, day_off_date=h_d).count()
            if emp_days_off != 0:
                raise ValidationError({'detail': 'Daxil edilmiş tarixlər arasında artıq icazə olaraq əlavə edilmiş tarixlər var.'})
            
            emp_holiday = employee_holiday_list().filter(employee=employee, holiday_date=h_d).count()
            if emp_holiday != 0:
                raise ValidationError({'detail': 'Daxil edilmiş tarixlər arasında artıq tətil olaraq əlavə edilmiş tarixlər var.'})

    employee_list = [emp.pk for emp in employees]
    person_on_duty_list = [p_d.pk for p_d in person_on_duty]

    transaction.on_commit(lambda: holiday_operation_create_task.delay(holiday_date_list, employee_list, person_on_duty_list))
    
    obj = HolidayOperation.objects.create(
        holiday_date=holiday_date_list, 
        holding=holding, 
        company=company,
        office=office,
    )
    if person_on_duty is not None:
        obj.person_on_duty.set(person_on_duty)
    obj.full_clean()
    obj.save()

    return obj

def employee_holiday_history_update(instance, **data):
    obj = employee_holiday_history_list().filter(id=instance.id).update(**data)
    return obj

def employee_holiday_history_delete(instance):
    emp_holidays = employee_holiday_list().filter(history=instance)
    for emp_holiday in emp_holidays:
        employee = emp_holiday.employee
        holiday_date = emp_holiday.holiday_date
        employee_working_day_increase(employee=employee, holiday_date=holiday_date)
    
    instance.delete()

def holiday_history_delete_service(instance_list):
    for instance in instance_list:
        employee_holiday_history_delete(instance=instance)
