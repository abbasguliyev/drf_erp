from django.contrib import admin

from holiday.models import (
    HoldingWorkingDay,
    EmployeeWorkingDay,
    TeamWorkingDay,
    OfficeWorkingDay,
    CompanyWorkingDay,
    SectionWorkingDay,
    PositionWorkingDay,
    HoldingExceptionWorker,
    TeamExceptionWorker,
    CompanyExceptionWorker,
    OfficeExceptionWorker,
    SectionExceptionWorker,
    PositionExceptionWorker
)

# Register your models here.
admin.site.register(HoldingWorkingDay)
admin.site.register(TeamWorkingDay)
admin.site.register(OfficeWorkingDay)
admin.site.register(CompanyWorkingDay)
admin.site.register(SectionWorkingDay)
admin.site.register(PositionWorkingDay)
admin.site.register(HoldingExceptionWorker)
admin.site.register(TeamExceptionWorker)
admin.site.register(CompanyExceptionWorker)
admin.site.register(SectionExceptionWorker)
admin.site.register(OfficeExceptionWorker)
admin.site.register(PositionExceptionWorker)


@admin.register(EmployeeWorkingDay)
class EmployeeWorkingDayAdmin(admin.ModelAdmin):
    list_filter = [
        "employee__id",
        "date"
    ]
    list_display = (
        "id",
        "employee",
        "date",
        "working_days_count",
        "non_working_days_count",
        "holidays",
        "paid_leave_days",
        "unpaid_leave_days",
        "is_paid",
        "payment_amount",
    )

