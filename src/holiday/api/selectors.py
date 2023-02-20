from django.db.models.query import QuerySet

from holiday.models import (
    EmployeeWorkingDay,
    EmployeeHolidayHistory,
    EmployeeHoliday,
    HolidayOperation,
    EmployeeDayOff,
    EmployeeDayOffHistory,
    EmployeeDayOffOperation
)

def employee_working_day_list(*, filters=None) -> QuerySet[EmployeeWorkingDay]:
    filters = filters or {}
    qs = EmployeeWorkingDay.objects.select_related('employee').all()
    return qs

def employee_holiday_history_list(*, filters=None) -> QuerySet[EmployeeHolidayHistory]:
    filters = filters or {}
    qs = EmployeeHolidayHistory.objects.select_related('employee').all()
    return qs

def employee_holiday_list(*, filters=None) -> QuerySet[EmployeeHoliday]:
    filters = filters or {}
    qs = EmployeeHoliday.objects.select_related('employee', 'history').all()
    return qs

def holiday_operation_list(*, filters=None) -> QuerySet[HolidayOperation]:
    filters = filters or {}
    qs = HolidayOperation.objects.select_related('company', 'office').prefetch_related('person_on_duty').all()
    return qs

def employee_day_off_history_list(*, filters=None) -> QuerySet[EmployeeDayOffHistory]:
    filters = filters or {}
    qs = EmployeeDayOffHistory.objects.select_related('employee').all()
    return qs

def employee_day_off_list(*, filters=None) -> QuerySet[EmployeeDayOff]:
    filters = filters or {}
    qs = EmployeeDayOff.objects.select_related('employee', 'history').all()
    return qs

def employee_day_off_operation_list(*, filters=None) -> QuerySet[EmployeeDayOffOperation]:
    filters = filters or {}
    qs = EmployeeDayOffOperation.objects.prefetch_related('employee').all()
    return qs

