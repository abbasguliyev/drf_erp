from datetime import date
from rest_framework.exceptions import ValidationError

from api.v1.cashbox.utils import calculate_holding_total_balance
from salary.models import (
    AdvancePayment,
    SalaryView,
    SalaryPunishment,
    SalaryDeduction,
    Bonus,
    PaySalary,
    MonthRange,
    SaleRange,
    CommissionInstallment,
    CommissionSaleRange, Commission
)
import pandas as pd

from .decorators import cashbox_expense_and_cash_flow_create


@cashbox_expense_and_cash_flow_create
def advancepayment_create(
        user,
        employee,
        amount: float = None,
        note: str = None,
        date: date = None
) -> AdvancePayment:
    """
    İşçiyə avans vermə funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})

    now = date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)

    user_advanced_payment = AdvancePayment.objects.filter(employee=employee,
                                                          date=f"{date.year}-{date.month}-{1}").count()
    if user_advanced_payment > 2:
        raise ValidationError({"detail": "Bir işçiyə eyni ay ərzində maksimum 2 dəfə avans verilə bilər"})

    salary_view = SalaryView.objects.get(employee=employee, date=f"{now.year}-{now.month}-{1}")
    next_month_salary_view = SalaryView.objects.get(employee=employee, date=f"{date.year}-{date.month}-{1}")

    amount = (float(next_month_salary_view.final_salary) * 15) / 100
    amount_after_advancedpayment = next_month_salary_view.final_salary - float(amount)

    salary_view.amount = amount
    next_month_salary_view.final_salary = amount_after_advancedpayment

    salary_view.save()
    next_month_salary_view.save()

    advance_payment = AdvancePayment.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date
    )
    advance_payment.full_clean()
    advance_payment.save()

    return advance_payment


def salarypunishment_create(
        *, employee,
        amount: float = None,
        note: str = None,
        date: date = None
) -> SalaryPunishment:
    """
    İşçinin maaşından cərimə tutmaq funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})

    if (amount == None):
        raise ValidationError({"detail": "Məbləği daxil edin"})

    now = date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)

    salary_view = SalaryView.objects.get(employee=employee, date=next_m)
    salary_view.final_salary = salary_view.final_salary - float(amount)

    salary_view.save()

    salary_punishment = SalaryPunishment.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date
    )

    salary_punishment.full_clean()
    salary_punishment.save()

    return salary_punishment


def salarydeduction_create(
        *, employee,
        amount: float = None,
        note: str = None,
        date: date = None
) -> SalaryDeduction:
    """
    İşçinin maaşından kəsinti tutmaq funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})

    if (amount == None):
        raise ValidationError({"detail": "Məbləği daxil edin"})

    now = date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)

    salary_view = SalaryView.objects.get(employee=employee, date=next_m)
    salary_view.final_salary = salary_view.final_salary - float(amount)

    salary_view.save()

    salary_deduction = SalaryDeduction.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date
    )

    salary_deduction.full_clean()
    salary_deduction.save()

    return salary_deduction


def bonus_create(
        *, employee,
        amount: float = None,
        note: str = None,
        date: date = None
) -> Bonus:
    """
    İşçilərə bonus vermək funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})

    if (amount == None):
        raise ValidationError({"detail": "Məbləği daxil edin"})

    now = date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)

    salary_view = SalaryView.objects.get(employee=employee, date=next_m)
    salary_view.final_salary = salary_view.final_salary + float(amount)

    salary_view.save()

    bonus = Bonus.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date
    )

    bonus.full_clean()
    bonus.save()

    return bonus


@cashbox_expense_and_cash_flow_create
def salary_pay_create(
        user,
        employee,
        amount: float = None,
        note: str = None,
        date: date = None,
        salary_date: date = date.today()
) -> PaySalary:
    """
    İşçilərə maaş vermək funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})

    now = date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)

    total_payed_amount = 0

    salary_view = SalaryView.objects.get(employee=employee, date=f"{now.year}-{now.month}-{1}")

    if salary_view.is_done == True:
        raise ValidationError({"detail": "İşçinin maaşını artıq ödəmisiniz"})

    amount = salary_view.final_salary
    total_payed_amount += float(amount)
    salary_view.final_salary = 0
    salary_view.is_done = True
    salary_view.save()

    salary_pay = PaySalary.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date,
        salary_date=salary_date
    )

    salary_pay.full_clean()
    salary_pay.save()

    return salary_pay


def month_range_create(start_month: int, end_month: int) -> MonthRange:
    if int(start_month) > int(end_month):
        raise ValidationError({'detail': 'Ay aralığını doğru daxil edin'})
    title = f"{start_month}-{end_month}"

    mr = MonthRange.objects.filter(title=title).count()
    if mr > 0:
        raise ValidationError({'detail': 'Bu aralıq artıq daxil edilib'})

    obj = MonthRange.objects.create(title=title, start_month=start_month, end_month=end_month)
    obj.full_clean()
    obj.save()

    return obj


def sale_range_create(start_count: int, end_count: int) -> SaleRange:
    if int(start_count) > int(end_count):
        raise ValidationError({'detail': 'Satış aralığını doğru daxil edin'})
    title = f"{start_count}-{end_count}"

    mr = SaleRange.objects.filter(title=title).count()
    if mr > 0:
        raise ValidationError({'detail': 'Bu aralıq artıq daxil edilib'})

    obj = SaleRange.objects.create(title=title, start_count=start_count, end_count=end_count)
    obj.full_clean()
    obj.save()

    return obj


def commission_installment_create(month_range, amount: float) -> CommissionInstallment:
    obj = CommissionInstallment.object.create(month_range=month_range, amount=amount)
    obj.full_clean()
    obj.save()

    return obj


def commission_sale_range_create(month_range, amount: float, sale_type: str) -> CommissionSaleRange:
    obj = CommissionSaleRange.object.create(month_range=month_range, amount=amount, sale_type=sale_type)
    obj.full_clean()
    obj.save()

    return obj


def commission_create(
        *, commission_name: str,
        for_office: float = 0,
        cash: float = 0,
        for_team: float = 0,
        month_ranges: str = None,
        sale_ranges: str = None,
) -> Commission:
    commission = Commission.objects.create(
        commission_name=commission_name,
        for_office=for_office,
        cash=cash,
        for_team=for_team
    )

    month_ranges_str = month_ranges
    if month_ranges_str is not None:
        month_ranges_list = month_ranges_str.split(',')
    else:
        month_ranges_list = None

    sale_ranges_str = sale_ranges
    if sale_ranges_str is not None:
        sale_ranges_list = sale_ranges_str.split(',')
    else:
        sale_ranges_list = None

    if month_ranges_list is not None:
        ci = CommissionInstallment.objects.bulk_create([
            CommissionInstallment(month_range=mr[0], amount=mr[1]) for mr in month_ranges_list
        ])
        ci.save()

    if sale_ranges_list is not None:
        cs = CommissionSaleRange.objects.bulk_create([
            CommissionSaleRange(sale_range=sr[0], amount=sr[1], sale_type=sr[2]) for sr in sale_ranges_list
        ])
        cs.save()

    commission.full_clean()
    commission.save()

    return commission