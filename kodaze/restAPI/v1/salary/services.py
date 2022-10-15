import pandas as pd
from company.models import (
    Holding,
)
from cashbox.models import (
    HoldingCashbox, 
    OfficeCashbox, 
    CompanyCashbox, 
)
from income_expense.models import (
    HoldingCashboxExpense, 
    OfficeCashboxExpense, 
    CompanyCashboxExpense
)
from salary.models import AdvancePayment, SalaryView
from rest_framework import status

from rest_framework.response import Response
import datetime

from restAPI.v1.cashbox.utils import (
    calculate_holding_total_balance, 
    cashflow_create, 
    calculate_office_balance, 
    calculate_company_balance, 
    calculate_holding_balance
)
def salary_pay_create(self, request, *args, **kwargs):
    """
    İşçilərə maaş vermək funksiyası
    """
    serializer = self.get_serializer(data=request.data)
    user = self.request.user
    # employees = serializer.data.get("employee")

    if serializer.is_valid():
        employee = serializer.validated_data.get("employee")
        note = serializer.validated_data.get("note")
        salary_date = serializer.validated_data.get("salary_date")
        if (serializer.validated_data.get("salary_date") == None):
            salary_date = datetime.date.today()
        if (serializer.validated_data.get("salary_date") == ""):
            salary_date = datetime.date.today()

        now = datetime.date.today()
        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)

        yekun_odenen_amount = 0
        try:
            salary_view = SalaryView.objects.get(employee=employee, date=f"{now.year}-{now.month}-{1}")
        except:
            return Response({"detail": f"{employee} işçinin maaş kartında xəta var"}, status=status.HTTP_404_NOT_FOUND)

        if salary_view.is_done == True:
            return Response({"detail": "İşçinin maaşını artıq ödəmisiniz"}, status=status.HTTP_400_BAD_REQUEST)

        amount = salary_view.final_salary
        yekun_odenen_amount += float(amount)
        salary_view.final_salary = 0
        office = employee.office
        company = employee.company
        holding = Holding.objects.all()[0]

        initial_balance = calculate_holding_total_balance()
        try:
            office_initial_balance = calculate_office_balance(office=office)
        except:
            pass
        try:
            company_initial_balance = calculate_company_balance(company=company)
        except:
            pass
            
        try:
            holding_initial_balance = calculate_holding_balance()
        except:
            pass

        note = f"{user.fullname} tərəfindən {employee.fullname} adlı işçiyə {amount} AZN maaş ödəndi"

        if office is not None:
            cashbox = OfficeCashbox.objects.get(office=office)
            if float(cashbox.balance) < float(amount):
                return Response({"detail": "Officein kassasında yetəri qədər məbləğ yoxdur"})
            cashbox.balance = float(cashbox.balance) - float(amount)
            cashbox.save()
            cashbox_expense = OfficeCashboxExpense.objects.create(
                executor=user,
                cashbox=cashbox,
                amount=amount,
                date=salary_date,
                note=note
            )
            cashbox_expense.save()

            subsequent_balance = calculate_holding_total_balance()
            office_subsequent_balance = calculate_office_balance(office=office)
            cashflow_create(
                office=office,
                company= office.company,
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
                return Response({"detail": "Şirkətin kassasında yetəri qədər məbləğ yoxdur"})
            cashbox.balance = float(cashbox.balance) - float(amount)
            cashbox.save()
            cashbox_expense = CompanyCashboxExpense.objects.create(
                executor=user,
                cashbox=cashbox,
                amount=amount,
                date=salary_date,
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
                return Response({"detail": "Holdingin kassasında yetəri qədər məbləğ yoxdur"})
            cashbox.balance = float(cashbox.balance) - float(amount)
            cashbox.save()
            cashbox_expense = HoldingCashboxExpense.objects.create(
                executor=user,
                cashbox=cashbox,
                amount=amount,
                date=salary_date,
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

        salary_view.is_done = True
        salary_view.save()
        serializer.save(amount=yekun_odenen_amount, salary_date=salary_date)
        return Response({"detail": "Maaş ödəmə yerinə yetirildi"}, status=status.HTTP_201_CREATED)

def bonus_create(self, request, *args, **kwargs):
    """
    İşçilərə bonus vermək funksiyası
    """
    serializer = self.get_serializer(data=request.data)
    user = self.request.user
    if serializer.is_valid():
        employee = serializer.validated_data.get("employee")
        amount = serializer.validated_data.get("amount")
        note = serializer.validated_data.get("note")
        date = serializer.validated_data.get("date")
        if (serializer.validated_data.get("date") == None):
            return Response({"detail": "Tarixi daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
        if (serializer.validated_data.get("amount") == None):
            return Response({"detail": "Məbləği daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.date.today()
        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)

        salary_view = SalaryView.objects.get(employee=employee, date=next_m)
        salary_view.final_salary = salary_view.final_salary + float(amount)

        office = employee.office

        company = employee.company

        holding = Holding.objects.all()[0]

        note = f"{user.fullname} tərəfindən {employee.fullname} adlı işçiyə {amount} AZN bonus"

        # if office is not None:
        #     cashbox = OfficeCashbox.objects.get(office=office)
        #     if float(cashbox.balance) < float(amount):
        #         return Response({"detail": "Officein kassasında yetəri qədər məbləğ yoxdur"})
        #     cashbox.balance = float(cashbox.balance) - float(amount)
        #     cashbox.save()
        #     cashbox_expense = OfficeCashboxExpense.objects.create(
        #         executor=user,
        #         cashbox=cashbox,
        #         amount=amount,
        #         date=date,
        #         note=note
        #     )
        #     cashbox_expense.save()
        # elif office == None and company is not None:
        #     cashbox = CompanyCashbox.objects.get(company=company)
        #     if float(cashbox.balance) < float(amount):
        #         return Response({"detail": "Şirkətin kassasında yetəri qədər məbləğ yoxdur"})
        #     cashbox.balance = float(cashbox.balance) - float(amount)
        #     cashbox.save()
        #     cashbox_expense = CompanyCashboxExpense.objects.create(
        #         executor=user,
        #         cashbox=cashbox,
        #         amount=amount,
        #         date=date,
        #         note=note
        #     )
        #     cashbox_expense.save()
        # elif office == None and company == None and holding is not None:
        #     cashbox = HoldingCashbox.objects.get(holding=holding)
        #     if float(cashbox.balance) < float(amount):
        #         return Response({"detail": "Holdingin kassasında yetəri qədər məbləğ yoxdur"})
        #     cashbox.balance = float(cashbox.balance) - float(amount)
        #     cashbox.save()
        #     cashbox_expense = HoldingCashboxExpense.objects.create(
        #         executor=user,
        #         cashbox=cashbox,
        #         amount=amount,
        #         date=date,
        #         note=note
        #     )
        #     cashbox_expense.save()

        salary_view.save()
        serializer.save(date=date)

        return Response({"detail": "Bonus əlavə olundu"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)

def salarydeduction_create(self, request, *args, **kwargs):
    """
    İşçinin maaşından kəsinti tutmaq funksiyası
    """
    serializer = self.get_serializer(data=request.data)
    user = self.request.user
    if serializer.is_valid():
        employee = serializer.validated_data.get("employee")
        amount = serializer.validated_data.get("amount")
        note = serializer.validated_data.get("note")
        date = serializer.validated_data.get("date")
        if (serializer.validated_data.get("date") == None):
            return Response({"detail": "Tarixi daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
        if (serializer.validated_data.get("amount") == None):
            return Response({"detail": "Məbləği daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.date.today()
        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)

        salary_view = SalaryView.objects.get(employee=employee, date=next_m)
        salary_view.final_salary = salary_view.final_salary - float(amount)
        office = employee.office
        company = employee.company
        holding = Holding.objects.all()[0]
        note = f"{user.fullname} tərəfindən {employee.fullname} adlı işçinin maaşından {amount} AZN kəsinti"

        # if office is not None:
        #     cashbox = OfficeCashbox.objects.get(office=office)
        #     cashbox.balance = float(cashbox.balance) + float(amount)
        #     cashbox.save()
        #     cashbox_income = OfficeCashboxIncome.objects.create(
        #         executor=user,
        #         cashbox=cashbox,
        #         amount=amount,
        #         date=date,
        #         note=note
        #     )
        #     cashbox_income.save()
        # elif office == None and company is not None:
        #     cashbox = CompanyCashbox.objects.get(company=company)
        #     cashbox.balance = float(cashbox.balance) + float(amount)
        #     cashbox.save()
        #     cashbox_income = CompanyCashboxIncome.objects.create(
        #         executor=user,
        #         cashbox=cashbox,
        #         amount=amount,
        #         date=date,
        #         note=note
        #     )
        #     cashbox_income.save()
        # elif office == None and company == None and holding is not None:
        #     cashbox = HoldingCashbox.objects.get(holding=holding)
        #     cashbox.balance = float(cashbox.balance) + float(amount)
        #     cashbox.save()
        #     cashbox_income = HoldingCashboxIncome.objects.create(
        #         executor=user,
        #         cashbox=cashbox,
        #         amount=amount,
        #         date=date,
        #         note=note
        #     )
        #     cashbox_income.save()

        salary_view.save()
        serializer.save(date=date)
        return Response({"detail": "Kəsinti əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)

def salarypunishment_create(self, request, *args, **kwargs):
    """
    İşçinin maaşından cərimə tutmaq funksiyası
    """
    serializer = self.get_serializer(data=request.data)
    user = self.request.user
    if serializer.is_valid():
        employee = serializer.validated_data.get("employee")
        amount = serializer.validated_data.get("amount")
        note = serializer.validated_data.get("note")
        date = serializer.validated_data.get("date")
        if (serializer.validated_data.get("date") == None):
            return Response({"detail": "Tarixi daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
        if (serializer.validated_data.get("amount") == None):
            return Response({"detail": "Məbləği daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.date.today()
        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)

        salary_view = SalaryView.objects.get(employee=employee, date=next_m)
        salary_view.final_salary = salary_view.final_salary - float(amount)
        office = employee.office
        company = employee.company
        holding = Holding.objects.all()[0]
        note = f"{user.fullname} tərəfindən {employee.fullname} adlı işçinin maaşından {amount} AZN cərimə"

        # if office is not None:
        #     cashbox = OfficeCashbox.objects.get(office=office)
        #     cashbox.balance = float(cashbox.balance) + float(amount)
        #     cashbox.save()
        #     cashbox_income = OfficeCashboxIncome.objects.create(
        #         executor=user,
        #         cashbox=cashbox,
        #         amount=amount,
        #         date=date,
        #         note=note
        #     )
        #     cashbox_income.save()
        # elif office == None and company is not None:
        #     cashbox = CompanyCashbox.objects.get(company=company)
        #     cashbox.balance = float(cashbox.balance) + float(amount)
        #     cashbox.save()
        #     cashbox_income = CompanyCashboxIncome.objects.create(
        #         executor=user,
        #         cashbox=cashbox,
        #         amount=amount,
        #         date=date,
        #         note=note
        #     )
        #     cashbox_income.save()
        # elif office == None and company == None and holding is not None:
        #     cashbox = HoldingCashbox.objects.get(holding=holding)
        #     cashbox.balance = float(cashbox.balance) + float(amount)
        #     cashbox.save()
        #     cashbox_income = HoldingCashboxIncome.objects.create(
        #         executor=user,
        #         cashbox=cashbox,
        #         amount=amount,
        #         date=date,
        #         note=note
        #     )
        #     cashbox_income.save()

        salary_view.save()
        serializer.save(date=date)
        return Response({"detail": "Cərimə əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)


def advancepayment_create(self, request, *args, **kwargs):
    """
    İşçiyə avans vermə funksiyası
    """
    serializer = self.get_serializer(data=request.data)
    user = self.request.user
    if serializer.is_valid():
        employee = serializer.validated_data.get("employee")
        note = serializer.validated_data.get("note")
        date = serializer.validated_data.get("date")
        if (serializer.validated_data.get("date") == None):
            return Response({"detail": "Tarixi daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.date.today()
        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)

        user_advanced_payment = AdvancePayment.objects.filter(employee=employee, date=f"{date.year}-{date.month}-{1}").count()
        if user_advanced_payment > 2:
            return Response({"detail": "Bir işçiyə eyni ay ərzində maksimum 2 dəfə avans verilə bilər"}, status=status.HTTP_400_BAD_REQUEST)

        salary_view = SalaryView.objects.get(employee=employee, date=f"{now.year}-{now.month}-{1}")
        next_month_salary_view = SalaryView.objects.get(employee=employee, date=f"{date.year}-{date.month}-{1}")

        amount = (float(next_month_salary_view.final_salary) * 15) / 100
        amount_after_advancedpayment = next_month_salary_view.final_salary - float(amount)
        initial_balance = calculate_holding_total_balance()
        
        salary_view.amount = amount
        next_month_salary_view.final_salary = amount_after_advancedpayment

        office = employee.office
        company = employee.company
        holding = Holding.objects.all()[0]

        office_initial_balance = calculate_office_balance(office=office)
        company_initial_balance = calculate_company_balance(company=company)
        holding_initial_balance = calculate_holding_balance()

        note = f"{user.fullname} tərəfindən {employee.fullname} adlı işçiyə {amount} AZN avans verildi"

        if office is not None:
            cashbox = OfficeCashbox.objects.get(office=office)
            if float(cashbox.balance) < float(amount):
                return Response({"detail": "Ofisin kassasında yetəri qədər məbləğ yoxdur"})
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
                return Response({"detail": "Şirkətin kassasında yetəri qədər məbləğ yoxdur"})
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
                return Response({"detail": "Holdingin kassasında yetəri qədər məbləğ yoxdur"})
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

        salary_view.save()
        next_month_salary_view.save()
        serializer.save(amount=amount, date=date)
        return Response({"detail": "Avans vermə əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)