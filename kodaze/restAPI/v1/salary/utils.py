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
from salary.models import SalaryView
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
def salary_ode_create(self, request, *args, **kwargs):
    """
    İşçilərə salary vermək funksiyası
    """
    serializer = self.get_serializer(data=request.data)
    user = self.request.user
    # employeeler = serializer.data.get("employee")

    if serializer.is_valid():
        employeeler = serializer.validated_data.get("employee")
        note = serializer.validated_data.get("note")
        installment = serializer.validated_data.get("installment")
        if (serializer.validated_data.get("installment") == None):
            installment = datetime.date.today()
        if (serializer.validated_data.get("installment") == ""):
            installment = datetime.date.today()

        now = datetime.date.today()
        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)

        yekun_odenen_amount = 0
        for employee in employeeler:
            try:
                salary_goruntuleme = SalaryView.objects.get(employee=employee, date=f"{now.year}-{now.month}-{1}")
            except:
                return Response({"detail": f"{employee} işçinin maaş kartında xəta var"}, status=status.HTTP_404_NOT_FOUND)

            amount = salary_goruntuleme.final_salary
            yekun_odenen_amount += float(amount)
            salary_goruntuleme.final_salary = 0
            office = employee.office
            company = employee.company
            holding = Holding.objects.all()[0]

            initial_balance = calculate_holding_total_balance()
            office_initial_balance = calculate_office_balance(office=office)
            company_initial_balance = calculate_company_balance(company=company)
            holding_initial_balance = calculate_holding_balance()

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
                    expense_datei=installment,
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
                    expense_datei=installment,
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
                    expense_datei=installment,
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

            salary_goruntuleme.is_done = True
            salary_goruntuleme.save()
        serializer.save(amount=yekun_odenen_amount, installment=installment)
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
            date = datetime.date.today()
        elif (serializer.validated_data.get("date") == ""):
            date = datetime.date.today()

        now = datetime.date.today()
        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)

        salary_goruntuleme = SalaryView.objects.get(employee=employee, date=next_m)
        salary_goruntuleme.final_salary = salary_goruntuleme.final_salary + float(amount)
        

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
        #         expense_datei=date,
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
        #         expense_datei=date,
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
        #         expense_datei=date,
        #         note=note
        #     )
        #     cashbox_expense.save()

        salary_goruntuleme.save()
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
            date = datetime.date.today()
        elif (serializer.validated_data.get("date") == ""):
            date = datetime.date.today()

        now = datetime.date.today()
        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)

        salary_goruntuleme = SalaryView.objects.get(employee=employee, date=next_m)
        salary_goruntuleme.final_salary = salary_goruntuleme.final_salary - float(amount)
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

        salary_goruntuleme.save()
        serializer.save(date=date)


        return Response({"detail": "Kəsinti əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)

def advancepayment_create(self, request, *args, **kwargs):
    """
    İşçiyə advancepayment vermə funksiyası
    """
    serializer = self.get_serializer(data=request.data)
    user = self.request.user
    if serializer.is_valid():
        employeeler = serializer.validated_data.get("employee")
        amount = serializer.validated_data.get("amount")
        note = serializer.validated_data.get("note")
        date = serializer.validated_data.get("date")
        if (serializer.validated_data.get("date") == None):
            date = datetime.date.today()
        elif (serializer.validated_data.get("date") == ""):
            date = datetime.date.today()

        now = datetime.date.today()
        d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)


        for employee in employeeler:
            salary_goruntuleme = SalaryView.objects.get(employee=employee, date=f"{now.year}-{now.month}-{1}")
            half_month_salary = serializer.validated_data.get("half_month_salary")
            if half_month_salary is not None:
                amount = (float(salary_goruntuleme.final_salary) * int(half_month_salary)) / 100

            advancepaymentdan_sonra_qalan_amount = salary_goruntuleme.final_salary - float(amount)

            initial_balance = calculate_holding_total_balance()
            if float(amount) > salary_goruntuleme.final_salary:
                return Response({"detail": "Daxil etdiyiniz məbləğ işçinin yekun maaşından daha çoxdur"}, status=status.HTTP_400_BAD_REQUEST)

            salary_goruntuleme.amount = amount
            salary_goruntuleme.final_salary = advancepaymentdan_sonra_qalan_amount

            office = employee.office
            company = employee.company
            holding = Holding.objects.all()[0]

            office_initial_balance = calculate_office_balance(office=office)
            company_initial_balance = calculate_company_balance(company=company)
            holding_initial_balance = calculate_holding_balance()

            note = f"{user.fullname} tərəfindən {employee.fullname} adlı işçiyə {amount} AZN advancepayment verildi"

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
                    expense_datei=date,
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
                    expense_datei=date,
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
                    expense_datei=date,
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

            salary_goruntuleme.save()
        serializer.save(amount=amount, date=date)
        return Response({"detail": "AdvancePayment vermə əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)