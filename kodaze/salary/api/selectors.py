from django.db.models.query import QuerySet

from salary.models import (
    AdvancePayment,
    SalaryDeduction,
    SalaryPunishment,
    Bonus,
    PaySalary,
    SalaryView,
)

from salary.api.filters import (
    AdvancePaymentFilter,
    SalaryDeductionFilter,
    SalaryPunishmentFilter,
    BonusFilter,
    PaySalaryFilter,
    SalaryViewFilter,
)

def advance_payment_list(*, filters=None) -> QuerySet[AdvancePayment]:
    filters = filters or {}
    qs = AdvancePayment.objects.select_related('employee').all()
    return AdvancePaymentFilter(filters, qs).qs

def salary_deduction_list(*, filters=None) -> QuerySet[SalaryDeduction]:
    filters = filters or {}
    qs = SalaryDeduction.objects.select_related('employee').all()
    return SalaryDeductionFilter(filters, qs).qs

def salary_punishment_list(*, filters=None) -> QuerySet[SalaryPunishment]:
    filters = filters or {}
    qs = SalaryPunishment.objects.select_related('employee').all()
    return SalaryPunishmentFilter(filters, qs).qs

def bonus_list(*, filters=None) -> QuerySet[Bonus]:
    filters = filters or {}
    qs = Bonus.objects.select_related('employee').all()
    return BonusFilter(filters, qs).qs

def pay_salary_list(*, filters=None) -> QuerySet[PaySalary]:
    filters = filters or {}
    qs = PaySalary.objects.select_related('employee').all()
    return PaySalaryFilter(filters, qs).qs

def salary_view_list(*, filters=None) -> QuerySet[SalaryView]:
    filters = filters or {}
    qs = SalaryView.objects.select_related('employee').all()
    return SalaryViewFilter(filters, qs).qs


