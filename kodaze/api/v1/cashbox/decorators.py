from api.v1.cashbox.utils import (
    calculate_holding_total_balance,
    calculate_office_balance,
    calculate_company_balance,
    calculate_holding_balance, cashflow_create
)
from cashbox.models import OfficeCashbox, CompanyCashbox, HoldingCashbox
from company.models import Holding

from rest_framework.exceptions import ValidationError

from income_expense.models import OfficeCashboxExpense, CompanyCashboxExpense, HoldingCashboxExpense
from salary.models import SalaryView
import datetime

from django.contrib.auth import get_user_model

User = get_user_model()


def cashbox_expense_and_cash_flow_create(func):
    """
    Əməliyyat zamanı kassadan pul məxaric edən və pul axını səhifəsinə əməliyyat ilə bağlı məlumatlar əlavə
    edilən funksiyalarda istifadə olunmalı olan dekorator funksiyası.
    Kassadan pul çıxılmasını və pul axını səhifəsinə məlumatların əlavə edilməsini təmin edir.
    """
    def wrapper(*args, **kwargs):
        print(args)
        print(kwargs)
        employee = kwargs['employee']
        date = kwargs['date']
        note = kwargs['note']
        if func.__name__ == "advancepayment_create":
            if kwargs['amount'] is None:
                next_month_salary_view = SalaryView.objects.get(employee=employee, date=f"{date.year}-{date.month}-{1}")
                amount = (float(next_month_salary_view.final_salary) * 15) / 100
        if func.__name__ == "salary_pay_create":
            salary_view = SalaryView.objects.get(employee=employee, date=f"{date.year}-{date.month}-{1}")
            amount = float(salary_view.final_salary)
        else:
            amount = kwargs['amount']
        user = args[0]

        initial_balance = calculate_holding_total_balance()

        office = employee.office
        company = employee.company
        holding = Holding.objects.all()[0]

        if office is not None:
            office_initial_balance = calculate_office_balance(office=office)
        if company is not None:
            company_initial_balance = calculate_company_balance(company=company)
        if holding is not None:
            holding_initial_balance = calculate_holding_balance()

        if office is not None:
            cashbox = OfficeCashbox.objects.get(office=office)
            if float(cashbox.balance) < float(amount):
                raise ValidationError({"detail": "Ofisin kassasında yetəri qədər məbləğ yoxdur"})
            cashbox.balance = float(cashbox.balance) - float(amount)
            cashbox.save()
            cashbox_expense = OfficeCashboxExpense.objects.create(
                executor=user,
                cashbox=cashbox,
                amount=amount,
                date=date,
                note=note
            )
            cashbox_expense.save()

            subsequent_balance = calculate_holding_total_balance()
            office_subsequent_balance = calculate_office_balance(office=office)
            cashflow_create(
                office=office,
                company=office.company,
                description=note,
                initial_balance=initial_balance,
                subsequent_balance=subsequent_balance,
                office_initial_balance=office_initial_balance,
                office_subsequent_balance=office_subsequent_balance,
                executor=user,
                operation_style="MƏXARİC",
                quantity=float(amount)
            )
        elif office == None and company is not None:
            cashbox = CompanyCashbox.objects.get(company=company)
            if float(cashbox.balance) < float(amount):
                raise ValidationError({"detail": "Şirkətin kassasında yetəri qədər məbləğ yoxdur"})
            cashbox.balance = float(cashbox.balance) - float(amount)
            cashbox.save()
            cashbox_expense = CompanyCashboxExpense.objects.create(
                executor=user,
                cashbox=cashbox,
                amount=amount,
                date=date,
                note=note
            )
            cashbox_expense.save()

            subsequent_balance = calculate_holding_total_balance()
            company_subsequent_balance = calculate_company_balance(company=company)
            cashflow_create(
                company=company,
                description=note,
                initial_balance=initial_balance,
                subsequent_balance=subsequent_balance,
                company_initial_balance=company_initial_balance,
                company_subsequent_balance=company_subsequent_balance,
                executor=user,
                operation_style="MƏXARİC",
                quantity=float(amount)
            )

        elif office == None and company == None and holding is not None:
            cashbox = HoldingCashbox.objects.get(holding=holding)
            if float(cashbox.balance) < float(amount):
                raise ValidationError({"detail": "Holdingin kassasında yetəri qədər məbləğ yoxdur"})
            cashbox.balance = float(cashbox.balance) - float(amount)
            cashbox.save()
            cashbox_expense = HoldingCashboxExpense.objects.create(
                executor=user,
                cashbox=cashbox,
                amount=amount,
                date=date,
                note=note
            )
            cashbox_expense.save()

            subsequent_balance = calculate_holding_total_balance()
            holding_subsequent_balance = calculate_holding_balance()
            cashflow_create(
                holding=holding,
                description=note,
                initial_balance=initial_balance,
                subsequent_balance=subsequent_balance,
                holding_initial_balance=holding_initial_balance,
                holding_subsequent_balance=holding_subsequent_balance,
                executor=user,
                operation_style="MƏXARİC",
                quantity=float(amount)
            )

        func(*args, **kwargs)

    return wrapper

