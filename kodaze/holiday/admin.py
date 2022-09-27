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
admin.site.register(EmployeeWorkingDay)
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


