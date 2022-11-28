import datetime
from rest_framework.exceptions import ValidationError
from holiday.models import (
    EmployeeDayOff,
    EmployeeDayOffHistory,
    EmployeeDayOffOperation
)
from holiday.api.selectors import employee_working_day_list, employee_day_off_history_list, employee_day_off_list, employee_day_off_operation_list
from account.api.selectors import user_list

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
    holiday_date: datetime.date.today(),
    is_paid: bool = False
) -> EmployeeDayOffOperation:
    obj = EmployeeDayOffOperation.objects.create(employee=employee, holiday_date=holiday_date, is_paid=is_paid)
    obj.full_clean()
    obj.save()

    return obj