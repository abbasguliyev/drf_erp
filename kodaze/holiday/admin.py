from django.contrib import admin

from holiday.models import (
    EmployeeHoliday,
    EmployeeWorkingDay,
    EmployeeHolidayHistory,
    HolidayOperation
)


@admin.register(EmployeeWorkingDay)
class EmployeeWorkingDayAdmin(admin.ModelAdmin):
    list_filter = [
        "employee__id",
        "working_days_count",
        "date"
    ]
    list_display = (
        "id",
        "employee",
        "working_days_count",
        "date"
    )

@admin.register(EmployeeHoliday)
class EmployeeHolidayAdmin(admin.ModelAdmin):
    list_filter = [
        "employee__id",
        "history",
        "holiday_date"
    ]
    list_display = (
        "id",
        "employee",
        "history",
        "holiday_date"
    )

@admin.register(EmployeeHolidayHistory)
class EmployeeHolidayHistoryAdmin(admin.ModelAdmin):
    list_filter = [
        "note",
        "created_date"
    ]
    list_display = (
        "id",
        "note",
        "created_date"
    )

@admin.register(HolidayOperation)
class HolidayOperationAdmin(admin.ModelAdmin):
    list_filter = [
        "holding",
        "company",
        "office",
        "holiday_date"
    ]
    list_display = (
        "id",
        "holding",
        "company",
        "office",
        "holiday_date"
    )

