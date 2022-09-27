from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from company.models import Holding
from cashbox.models import HoldingCashbox, OfficeCashbox, CompanyCashbox

from restAPI.v1.cashbox.utils import holding_umumi_balance_hesabla, pul_axini_create, company_balance_hesabla, office_balance_hesabla, holding_balance_hesabla


# *************** Holding Kassa income expense ***************
def cashbox_income_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    amount = request.data.get("amount")
    user = request.user

    if(amount != None):
        holding = get_object_or_404(Holding, name="ALLIANCE")
        cashbox = get_object_or_404(HoldingCashbox, holding=holding)
        previous_balance=cashbox.balance

        initial_balance = holding_umumi_balance_hesabla()
        holding_initial_balance = holding_balance_hesabla()

        date = request.data.get("date")

        if(date == None):
            date = datetime.today().strftime('%d-%m-%Y')

        note = request.data.get("note")

        cashbox_balance = cashbox.balance

        yekun_balance = float(amount) + float(cashbox_balance)

        if(serializer.is_valid()):
            cashbox.balance = yekun_balance
            cashbox.save()

            sonraki_kassa_balance=cashbox.balance

            serializer.save(executor=user, cashbox=cashbox, date=date, previous_balance=previous_balance, subsequent_balance=sonraki_kassa_balance)

            subsequent_balance = holding_umumi_balance_hesabla()
            holding_subsequent_balance = holding_balance_hesabla()

            pul_axini_create(
                holding=holding,
                operation_style="MƏDAXİL",
                description=f"{holding.name} holdinq kassasına {float(amount)} AZN mədaxil edildi",
                initial_balance=initial_balance,
                subsequent_balance=subsequent_balance,
                holding_initial_balance=holding_initial_balance,
                holding_subsequent_balance=holding_subsequent_balance,
                executor=user,
                date=date,
                quantity=float(amount)
            )

            return Response({"detail": f"{holding} holdinqinə {amount} azn mədaxil edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məbləği daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

def cashbox_expense_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    amount = request.data.get("amount")

    user = request.user

    note = request.data.get("note")

    holding = get_object_or_404(Holding, name="ALLIANCE")
    cashbox = get_object_or_404(HoldingCashbox, holding=holding)
    previous_balance=cashbox.balance

    initial_balance = holding_umumi_balance_hesabla()
    holding_initial_balance = holding_balance_hesabla()

    cashbox_balance = cashbox.balance

    expense_datei = request.data.get("expense_datei")

    if(expense_datei == None):
        expense_datei = datetime.today().strftime('%d-%m-%Y')

    if(cashbox_balance != 0):
        if(amount != None):
            if(float(amount) <= float(cashbox_balance)):
                yekun_balance = float(cashbox_balance) - float(amount)
                if(serializer.is_valid()):
                    cashbox.balance = yekun_balance
                    cashbox.save()
                    
                    sonraki_kassa_balance=cashbox.balance

                    serializer.save(executor=user, cashbox=cashbox, expense_datei=expense_datei, previous_balance=previous_balance, subsequent_balance=sonraki_kassa_balance)

                    subsequent_balance = holding_umumi_balance_hesabla()
                    holding_subsequent_balance = holding_balance_hesabla()

                    pul_axini_create(
                        holding=holding,
                        operation_style="MƏXARİC",
                        description=f"{holding.name} holdinq kassasından {float(amount)} AZN məxaric edildi",
                        initial_balance=initial_balance,
                        subsequent_balance=subsequent_balance,
                        holding_initial_balance=holding_initial_balance,
                        holding_subsequent_balance=holding_subsequent_balance,
                        executor=user,
                        date=expense_datei,
                        quantity=float(amount)
                    )

                    return Response({"detail": f"{holding} holdinqindən {amount} azn məxaric edildi"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Daxil etdiyiniz məbləğ holdinqin balansıdan böyük ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Holdinqin balansı 0-dır"}, status=status.HTTP_400_BAD_REQUEST)

# *************** Company Kassa income expense ***************

def cashbox_income_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    amount = request.data.get("amount")
    user = request.user
    
    if(amount != ""):
        cashbox_id = request.data.get("cashbox_id")
        cashbox = get_object_or_404(CompanyCashbox, pk=cashbox_id)

        previous_balance=cashbox.balance

        company=cashbox.company

        date = request.data.get("date")

        initial_balance = holding_umumi_balance_hesabla()

        company_initial_balance = company_balance_hesabla(company=company)

        if(date == ""):
            date = datetime.today().strftime('%d-%m-%Y')

        note = request.data.get("note")

        cashbox_balance = cashbox.balance

        yekun_balance = float(amount) + float(cashbox_balance)

        if(serializer.is_valid()):
            cashbox.balance = yekun_balance
            cashbox.save()

            sonraki_kassa_balance=cashbox.balance

            serializer.save(executor=user, cashbox=cashbox, date=date, previous_balance=previous_balance, subsequent_balance=sonraki_kassa_balance)

            subsequent_balance = holding_umumi_balance_hesabla()
            company_subsequent_balance = company_balance_hesabla(company=company)
            pul_axini_create(
                company=company,
                operation_style="MƏDAXİL",
                description=f"{company.name} şirkət kassasına {float(amount)} AZN mədaxil edildi",
                initial_balance=initial_balance,
                subsequent_balance=subsequent_balance,
                company_initial_balance=company_initial_balance,
                company_subsequent_balance=company_subsequent_balance,
                executor=user,
                date=date,
                quantity=float(amount)
            )

            return Response({"detail": f"{cashbox.company} şirkətinə {amount} azn mədaxil edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məbləği daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

def cashbox_expense_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    amount = request.data.get("amount")

    user = request.user

    note = request.data.get("note")

    cashbox_id = request.data.get("cashbox_id")
    cashbox = get_object_or_404(CompanyCashbox, pk=cashbox_id)
    company=cashbox.company

    previous_balance=cashbox.balance

    initial_balance = holding_umumi_balance_hesabla()
    company_initial_balance = company_balance_hesabla(company=company)

    cashbox_balance = cashbox.balance

    expense_datei = request.data.get("expense_datei")

    if(expense_datei == ""):
        expense_datei = datetime.today().strftime('%d-%m-%Y')

    if(cashbox_balance != 0):
        if(amount != ""):
            if(float(amount) <= float(cashbox_balance)):
                yekun_balance = float(cashbox_balance) - float(amount)
                if(serializer.is_valid()):
                    cashbox.balance = yekun_balance
                    cashbox.save()
                    
                    sonraki_kassa_balance=cashbox.balance

                    serializer.save(executor=user, cashbox=cashbox, expense_datei=expense_datei, previous_balance=previous_balance, subsequent_balance=sonraki_kassa_balance)

                    subsequent_balance = holding_umumi_balance_hesabla()
                    company_subsequent_balance = company_balance_hesabla(company=company)
                    pul_axini_create(
                        company=company,
                        operation_style="MƏXARİC",
                        description=f"{company.name} şirkət kassasından {float(amount)} AZN məxaric edildi",
                        initial_balance=initial_balance,
                        subsequent_balance=subsequent_balance,
                        company_initial_balance=company_initial_balance,
                        company_subsequent_balance=company_subsequent_balance,
                        executor=user,
                        date=expense_datei,
                        quantity=float(amount)
                    )
                    return Response({"detail": f"{cashbox.company} şirkətindən {amount} azn məxaric edildi"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Daxil etdiyiniz məbləğ şirkətinin balansıdan böyük ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Şirkətin balansı 0-dır"}, status=status.HTTP_400_BAD_REQUEST)

# *************** Office Kassa income expense ***************

def cashbox_income_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    amount = request.data.get("amount")
    user = request.user

    if(amount != ""):
        cashbox_id = request.data.get("cashbox_id")
        cashbox = get_object_or_404(OfficeCashbox, pk=cashbox_id)
        date = request.data.get("date")
        office=cashbox.office
        previous_balance=cashbox.balance

        initial_balance = holding_umumi_balance_hesabla()
        office_initial_balance = office_balance_hesabla(office=office)
        if(date == ""):
            date = datetime.today().strftime('%d-%m-%Y')
        note = request.data.get("note")
        cashbox_balance = cashbox.balance
        yekun_balance = float(amount) + float(cashbox_balance)

        if(serializer.is_valid()):
            cashbox.balance = yekun_balance
            cashbox.save()
            sonraki_kassa_balance=cashbox.balance
            serializer.save(executor=user, cashbox=cashbox, date=date, previous_balance=previous_balance, subsequent_balance=sonraki_kassa_balance)
            subsequent_balance = holding_umumi_balance_hesabla()
            office_subsequent_balance = office_balance_hesabla(office=office)
            pul_axini_create(
                office=office,
                company=office.company,
                operation_style="MƏDAXİL",
                description=f"{office.name} office kassasına {float(amount)} AZN əlavə edildi",
                initial_balance=initial_balance,
                subsequent_balance=subsequent_balance,
                office_initial_balance=office_initial_balance,
                office_subsequent_balance=office_subsequent_balance,
                executor=user,
                date=date,
                quantity=float(amount)
            )
            return Response({"detail": f"{cashbox.office} officeinə {amount} azn mədaxil edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məbləği daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

def cashbox_expense_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    amount = request.data.get("amount")
    note = request.data.get("note")
    user = request.user

    cashbox_id = request.data.get("cashbox_id")
    cashbox = get_object_or_404(OfficeCashbox, pk=cashbox_id)
    office=cashbox.office
    previous_balance=cashbox.balance

    initial_balance = holding_umumi_balance_hesabla()

    office_initial_balance = office_balance_hesabla(office=office)

    cashbox_balance = cashbox.balance
    expense_datei = request.data.get("expense_datei")
    if(expense_datei == ""):
        expense_datei = datetime.today().strftime('%d-%m-%Y')

    if(cashbox_balance != 0):
        if(amount != ""):
            if(float(amount) <= float(cashbox_balance)):
                yekun_balance = float(cashbox_balance) - float(amount)
                if(serializer.is_valid()):
                    cashbox.balance = yekun_balance
                    cashbox.save()
                    sonraki_kassa_balance=cashbox.balance
                    serializer.save(executor=user, cashbox=cashbox, expense_datei=expense_datei, previous_balance=previous_balance, subsequent_balance=sonraki_kassa_balance)
                    subsequent_balance = holding_umumi_balance_hesabla()
                    office_subsequent_balance = office_balance_hesabla(office=office)
                    pul_axini_create(
                        office=office,
                        company=office.company,
                        operation_style="MƏXARİC",
                        description=f"{office.name} office kassasından {float(amount)} AZN məxaric edildi",
                        initial_balance=initial_balance,
                        subsequent_balance=subsequent_balance,
                        office_initial_balance=office_initial_balance,
                        office_subsequent_balance=office_subsequent_balance,
                        executor=user,
                        date=expense_datei,
                        quantity=float(amount)
                    )
                    return Response({"detail": f"{cashbox.office} officeindən {amount} azn məxaric edildi"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Daxil etdiyiniz məbləğ officein balansıdan böyük ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Officein balansı 0-dır"}, status=status.HTTP_400_BAD_REQUEST)