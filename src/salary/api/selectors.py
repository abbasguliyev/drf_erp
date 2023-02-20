from django.db.models.query import QuerySet

from salary.models import (
    AdvancePayment,
    SalaryDeduction,
    SalaryPunishment,
    Bonus,
    PaySalary,
    SalaryView,
    EmployeeActivityHistory,
    SaleRange,
    MonthRange,
)

def advance_payment_list(*, filters=None) -> QuerySet[AdvancePayment]:
    filters = filters or {}
    qs = AdvancePayment.objects.select_related('employee').all()
    return qs

def salary_deduction_list(*, filters=None) -> QuerySet[SalaryDeduction]:
    filters = filters or {}
    qs = SalaryDeduction.objects.select_related('employee').all()
    return qs

def salary_punishment_list(*, filters=None) -> QuerySet[SalaryPunishment]:
    filters = filters or {}
    qs = SalaryPunishment.objects.select_related('employee').all()
    return qs

def bonus_list(*, filters=None) -> QuerySet[Bonus]:
    filters = filters or {}
    qs = Bonus.objects.select_related('employee').all()
    return qs

def pay_salary_list(*, filters=None) -> QuerySet[PaySalary]:
    filters = filters or {}
    qs = PaySalary.objects.prefetch_related('salary_view').all()
    return qs

def salary_view_list(*, filters=None) -> QuerySet[SalaryView]:
    filters = filters or {}
    qs = SalaryView.objects.select_related('employee').all()
    return qs

def employee_activity_history_list(*, filters=None) -> QuerySet[EmployeeActivityHistory]:
    filters = filters or {}
    qs = EmployeeActivityHistory.objects.select_related('salary_view').all()
    return qs


def sale_range_list(*, filters=None) -> QuerySet[SaleRange]:
    filters = filters or {}
    qs = SaleRange.objects.all()
    return qs

def month_range_list(*, filters=None) -> QuerySet[MonthRange]:
    filters = filters or {}
    qs = MonthRange.objects.all()
    return qs
