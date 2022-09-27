import math
from rest_framework import status
from rest_framework.response import Response
from account.models import User, Customer
from restAPI.v1.contract.serializers import ContractSerializer
from company.models import Office, Section, Position
from cashbox.models import OfficeCashbox
from income_expense.models import OfficeCashboxIncome, OfficeCashboxExpense
from salary.models import (
    Manager1PrimNew, 
    SalaryView, 
    OfficeLeaderPrim, 
    GroupLeaderPrimNew
)
from contract.models import Installment
from warehouse.models import (
    Warehouse,
    Stock
)
from product.models import Product
from services.models import Service, ServicePayment
from rest_framework.generics import get_object_or_404
import pandas as pd
import datetime
import traceback
from services.signals import create_services

from restAPI.v1.utils.ocean_contract_pdf_create import (
    ocean_contract_pdf_canvas,
    ocean_create_contract_pdf,
    ocean_installment_contract_pdf_canvas,
    ocean_installment_create_contract_pdf,
)

from restAPI.v1.utils.magnus_contract_pdf_create import (
    magnus_create_contract_pdf,
    magnus_contract_pdf_canvas,
    magnus_installment_create_contract_pdf,
    magnus_installment_contract_pdf_canvas,
)

from restAPI.v1.cashbox.utils import (
    holding_umumi_balance_hesabla, 
    pul_axini_create, 
    office_balance_hesabla, 
)

import django

def create_and_add_pdf_when_contract_updated(sender, instance, created, **kwargs):
    if created:
        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.office.company.name == okean:
            contract_pdf_canvas_list = ocean_contract_pdf_canvas(
                contract=instance, customer=instance.customer
            )
            contract_pdf = ocean_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        elif instance.office.company.name == magnus:
            contract_pdf_canvas_list = magnus_contract_pdf_canvas(
                contract=instance, customer=instance.customer
            )
            contract_pdf = magnus_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        instance.pdf = contract_pdf
        instance.save()

def create_and_add_pdf_when_contract_installment_updated(sender, instance, created, **kwargs):
    if created:
        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.office.company.name == okean:
            contract_pdf_canvas_list = ocean_installment_contract_pdf_canvas(
                contract=instance
            )
            contract_pdf = ocean_installment_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        elif instance.office.company.name == magnus:
            contract_pdf_canvas_list = magnus_installment_contract_pdf_canvas(
                contract=instance
            )
            contract_pdf = magnus_installment_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        instance.pdf_elave = contract_pdf
        instance.save()

def pdf_create_when_contract_updated(sender, instance, created):
    create_and_add_pdf_when_contract_updated(
        sender=sender, instance=instance, created=created)
    create_and_add_pdf_when_contract_installment_updated(
        sender=sender, instance=instance, created=created)
# ----------------------------------------------------------------------------------------------------------------------

def reduce_product_from_stock(stock, product_quantity):
    stock.quantity = stock.quantity - int(product_quantity)
    stock.save()
    if (stock.quantity == 0):
        stock.delete()
    return stock.quantity


def add_product_to_stock(stock, product_quantity):
    stock.quantity = stock.quantity + int(product_quantity)
    stock.save()
    return stock.quantity


def c_income(company_cashbox, the_amount_to_enter, responsible_employee_1, note):
    total_balance = float(the_amount_to_enter) + float(company_cashbox.balance)
    company_cashbox.balance = total_balance
    company_cashbox.save()
    date = datetime.date.today()

    income = OfficeCashboxIncome.objects.create(
        executor=responsible_employee_1,
        office_cashbox=company_cashbox,
        amount=the_amount_to_enter,
        date=date,
        note=note
    )
    income.save()
    return income


def expense(company_cashbox, the_amount_to_enter, responsible_employee_1, note):
    total_balance = float(company_cashbox.balance) - float(the_amount_to_enter)
    company_cashbox.balance = total_balance
    company_cashbox.save()
    date = datetime.date.today()

    expense = OfficeCashboxExpense.objects.create(
        executor=responsible_employee_1,
        office_cashbox=company_cashbox,
        amount=the_amount_to_enter,
        date=date,
        note=note
    )
    expense.save()
    return expense

# ----------------------------------------------------------------------------------------------------------------------


def create_installment_when_update_contract(
    instance, loan_term, payment_style, initial_payment, initial_payment_debt,  **kwargs
):
    """
    Bu method ne zaman contract negd odenisden installmente kecirilerse o zaman ishe dushur.
    """

    loan_term = loan_term
    product_quantity = instance.product_quantity

    def loan_term_func(loan_term, product_quantity):
        new_loan_term = loan_term * product_quantity
        return new_loan_term

    if(payment_style == "KREDİT"):

        now = datetime.datetime.today().strftime('%d-%m-%Y')
        inc_month = pd.date_range(now, periods=loan_term+1, freq='M')

        initial_payment = initial_payment
        initial_payment_debt = initial_payment_debt

        if(initial_payment is not None):
            initial_payment = float(initial_payment)

        if(initial_payment_debt is not None):
            initial_payment_debt = float(initial_payment_debt)

        total_amount = instance.total_amount

        if(initial_payment_debt == 0):
            initial_payment_full = initial_payment
        elif(initial_payment_debt != 0):
            initial_payment_full = initial_payment + initial_payment_debt

        total_amount_to_be_paid_for_the_month = total_amount - initial_payment_full

        if(loan_term > 0):
            amount_to_be_paid_by_month = total_amount_to_be_paid_for_the_month // loan_term

            residue = amount_to_be_paid_by_month * (loan_term - 1)
            amount_to_be_paid_in_the_last_month = total_amount_to_be_paid_for_the_month - residue

            i = 1
            while(i <= loan_term):
                if(i == loan_term):
                    if(datetime.date.today().day < 29):
                        Installment.objects.create(
                            month_no=i,
                            contract=instance,
                            date=f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}",
                            price=amount_to_be_paid_in_the_last_month
                        ).save()
                    elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                        if(inc_month[i].day <= datetime.date.today().day):
                            Installment.objects.create(
                                month_no=i,
                                contract=instance,
                                date=f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                                price=amount_to_be_paid_in_the_last_month
                            ).save()
                        else:
                            Installment.objects.create(
                                month_no=i,
                                contract=instance,
                                date=f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}",
                                price=amount_to_be_paid_in_the_last_month,
                                last_month=True
                            ).save()
                else:
                    if(datetime.date.today().day < 29):
                        Installment.objects.create(
                            month_no=i,
                            contract=instance,
                            date=f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}",
                            price=amount_to_be_paid_by_month
                        ).save()
                    elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                        if(inc_month[i].day <= datetime.date.today().day):
                            Installment.objects.create(
                                month_no=i,
                                contract=instance,
                                date=f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                                price=amount_to_be_paid_by_month
                            ).save()
                        else:
                            Installment.objects.create(
                                month_no=i,
                                contract=instance,
                                date=f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}",
                                price=amount_to_be_paid_by_month
                            ).save()
                i += 1


def contract_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    user = None

    group_leader_id = request.data.get("group_leader_id")

    if (group_leader_id == None):
        user = self.request.user
    else:
        user = get_object_or_404(User, pk=group_leader_id)

    manager1_id = request.data.get("manager1_id")
    manager2_id = request.data.get("manager2_id")

    customer_id = request.data.get("customer_id")
    if customer_id == None:
        return Response({"detail": "Müştəri note olunmayıb"}, status=status.HTTP_400_BAD_REQUEST)
    customer = get_object_or_404(Customer, pk=customer_id)

    manager1 = None
    manager2 = None

    if (manager1_id is not None):
        try:
            manager1 = get_object_or_404(User, pk=manager1_id)
            if (manager2_id == None):
                manager2 = manager1
        except:
            return Response({"detail": "Manager1 tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    if (manager2_id is not None):
        try:
            manager2 = get_object_or_404(User, pk=manager2_id)
            if (manager1_id == None):
                manager1 = manager2
        except:
            return Response({"detail": "Manager2 tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    my_time = datetime.datetime.min.time()

    nowki_date_date = datetime.date.today()
    nowki_date = datetime.datetime.combine(nowki_date_date, my_time)
    nowki_date_san = datetime.datetime.timestamp(nowki_date)

    if (request.data.get("initial_payment_date") is not None):
        initial_payment_date = request.data.get("initial_payment_date")
        initial_payment_date_date = datetime.datetime.strptime(
            initial_payment_date, "%d-%m-%Y")
        initial_payment_date_san = datetime.datetime.timestamp(
            initial_payment_date_date)

    if (request.data.get("initial_payment_debt_date") is not None):
        initial_payment_debt_date = request.data.get(
            "initial_payment_debt_date")
        initial_payment_debt_date_date = datetime.datetime.strptime(
            initial_payment_debt_date, "%d-%m-%Y")
        initial_payment_debt_date_san = datetime.datetime.timestamp(
            initial_payment_debt_date_date)

    product_id_str = request.data.get("product_id")
    if (product_id_str == None):
        return Response({"detail": "Müqavilə imzalamaq üçün mütləq məhsul daxil edilməlidir."},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        product_id = int(product_id_str)

    try:
        product = get_object_or_404(Product, pk=product_id)
    except:
        return Response({"detail": "Məhsul tapılmadı"},
                        status=status.HTTP_400_BAD_REQUEST)

    product_quantity = request.data.get("product_quantity")
    if (product_quantity == None):
        product_quantity = 1

    payment_style = request.data.get("payment_style")

    initial_payment = request.data.get("initial_payment")

    initial_payment_debt = request.data.get("initial_payment_debt")

    def umumi_amount(product_pricei, product_quantity):
        total_amount = product_pricei * product_quantity
        return total_amount

    if (product_quantity == None):
        product_quantity = 1

    total_amount = umumi_amount(product.price, int(product_quantity))

    office_id = request.data.get("office_id")

    company_id = request.data.get("company_id")

    loan_term = request.data.get("loan_term")

    if (user.office == None):
        office = Office.objects.get(pk=office_id)
    else:
        office = user.office
    if (user.company == None):
        company = product.company
    else:
        company = user.company

    try:
        warehouse = get_object_or_404(Warehouse, office=office)
    except:
        traceback.print_exc()
        return Response({"detail": "Warehouse tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cashbox = get_object_or_404(OfficeCashbox, office=office)
    except:
        traceback.print_exc()
        return Response({"detail": "Office Kassa tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    cashbox_balance = cashbox.balance
    remaining_debt = 0

    try:
        try:
            stok = get_object_or_404(Stock, warehouse=warehouse, product=product)
        except:
            return Response({"detail": "Stockda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)
        if (stok.quantity < int(product_quantity)):
            return Response({"detail": "Stockda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

        if (serializer.is_valid()):
            if (product_quantity == None):
                product_quantity = 1
            # Kredit
            if (payment_style == "KREDİT"):
                if (loan_term == None):
                    # Kredit muddeti daxil edilmezse
                    return Response({"detail": "Ödəmə statusu installmentdir amma installment müddəti daxil edilməyib"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif (int(loan_term) == 0):
                    # Kredit muddeyi 0 daxil edilerse
                    return Response({"detail": "Ödəmə statusu installmentdir amma installment müddəti 0 daxil edilib"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif (int(loan_term) > 30):
                    # Kredit muddeti 31 ay daxil edilerse
                    return Response({"detail": "Maksimum installment müddəti 30 aydır"}, status=status.HTTP_400_BAD_REQUEST)
                elif (int(loan_term) > 0):
                    # Kredit muddeti 0-dan boyuk olarsa

                    if ((initial_payment is not None) and (request.data.get("initial_payment_date") == None)):
                        initial_payment_date = nowki_date_date
                        initial_payment_date_date = nowki_date
                        initial_payment_date_san = nowki_date_san

                    if ((initial_payment_debt is not None) and (request.data.get("initial_payment_debt_date") == None)):
                        return Response({
                            "detail": "Qalıq İlkin ödəniş məbləği note olunub amma qalıq ilkin ödəniş datei note olunmayıb"},
                            status=status.HTTP_400_BAD_REQUEST)

                    if (initial_payment == None and initial_payment_debt == None):
                        # Ilkin odenis daxil edilmezse
                        reduce_product_from_stock(stok, int(product_quantity))
                        total_amount = umumi_amount(
                            product.price, int(product_quantity))

                        remaining_debt = float(total_amount)

                        serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company, office=office,
                                        total_amount=total_amount, remaining_debt=remaining_debt)
                        # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                        #                 status=status.HTTP_201_CREATED)
                        return Response(data=serializer.data,
                                        status=status.HTTP_201_CREATED)
                    elif (initial_payment is not None and initial_payment_debt == None):
                        total_amount = umumi_amount(product.price, int(product_quantity))
                        if float(initial_payment) >= float(total_amount):
                            return Response({"detail": "İlkin ödəniş məbləği müqavilənin məbləğindən çox ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
                        # Umumi ilkin odenis amounti daxil edilerse ve qaliq ilkin odenis amounti daxil edilmezse
                        if (nowki_date_san == initial_payment_date_san):
                            reduce_product_from_stock(stok, int(product_quantity))
                            total_amount = umumi_amount(product.price, int(product_quantity))
                            
                            initial_balance = holding_umumi_balance_hesabla()
                            office_initial_balance = office_balance_hesabla(office=office)
                            note = f"GroupLeader - {user.fullname}, müştəri - {customer.fullname}, date - {initial_payment_date}, ödəniş üslubu - {payment_style}, tam ilkin ödəniş"
                            c_income(cashbox, float(
                                initial_payment), user, note)

                            remaining_debt = float(
                                total_amount) - float(initial_payment)
                            serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company,
                                            office=office, initial_payment=initial_payment,
                                            initial_payment_status="BİTMİŞ", total_amount=total_amount, remaining_debt=remaining_debt,)
                            subsequent_balance = holding_umumi_balance_hesabla()
                            office_subsequent_balance = office_balance_hesabla(office=office)
                            pul_axini_create(
                                office=office,
                                company=office.company,
                                description=f"GroupLeader - {user.fullname}, müştəri - {customer.fullname}, date - {initial_payment_date}, ödəniş üslubu - {payment_style}, tam ilkin ödəniş",
                                initial_balance=initial_balance,
                                subsequent_balance=subsequent_balance,
                                office_initial_balance=office_initial_balance,
                                office_subsequent_balance=office_subsequent_balance,
                                executor=user,
                                operation_style="MƏDAXİL",
                                quantity=float(initial_payment)
                            )
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)
                        elif (nowki_date_san < initial_payment_date_san):
                            reduce_product_from_stock(stok, int(product_quantity))
                            total_amount = umumi_amount(
                                product.price, int(product_quantity))

                            remaining_debt = float(
                                total_amount) - float(initial_payment)

                            serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company,
                                            office=office, initial_payment=initial_payment,
                                            initial_payment_status="DAVAM EDƏN", remaining_debt=remaining_debt,
                                            total_amount=total_amount)
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)
                        elif (nowki_date_san > initial_payment_date_san):
                            return Response({"detail": "İlkin ödəniş dateini keçmiş dateə təyin edə bilməzsiniz"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                        #                 status=status.HTTP_201_CREATED)
                        return Response(data=serializer.data,
                                        status=status.HTTP_201_CREATED)

                    elif ((initial_payment == None and initial_payment_debt is not None) or (
                            float(initial_payment) == 0 and initial_payment_debt is not None)):
                        return Response({"detail": "İlkin ödəniş daxil edilmədən qalıq ilkin ödəniş daxil edilə bilməz"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    elif (float(initial_payment) == 0):
                        # Umumi ilkin odenis amounti 0 olarsa
                        return Response({"detail": "İlkin ödəniş 0 azn daxil edilə bilməz"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    elif (initial_payment_debt is not None):
                        total_amount2 = umumi_amount(product.price, int(product_quantity))
                        remaining_debt2 = float(total_amount2) - float(initial_payment_debt)
                        if float(initial_payment) >= float(remaining_debt2):
                            return Response({"detail": "İlkin ödəniş qalıq məbləği qalıq məbləğdən çox ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
                        if ((nowki_date_san == initial_payment_date_san) and (
                                nowki_date_san < initial_payment_debt_date_san)):
                            reduce_product_from_stock(stok, int(product_quantity))
                            total_amount = umumi_amount(
                                product.price, int(product_quantity))

                            initial_balance = holding_umumi_balance_hesabla()
                            office_initial_balance = office_balance_hesabla(office=office)

                            note = f"GroupLeader - {user.fullname}, müştəri - {customer.fullname}, date - {initial_payment_date}, ödəniş üslubu - {payment_style}, 2-dəfəyə ilkin ödənişin birincisi."
                            c_income(cashbox, float(
                                initial_payment), user, note)

                            remaining_debt = float(total_amount) - float(initial_payment)

                            serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company,
                                            office=office, initial_payment=initial_payment,
                                            initial_payment_debt=initial_payment_debt, initial_payment_status="BİTMİŞ",
                                            initial_payment_debt_status="DAVAM EDƏN",
                                            total_amount=total_amount, remaining_debt=remaining_debt)
                            subsequent_balance = holding_umumi_balance_hesabla()
                            office_subsequent_balance = office_balance_hesabla(office=office)
                            pul_axini_create(
                                office=office,
                                company=office.company,
                                description=f"GroupLeader - {user.fullname}, müştəri - {customer.fullname}, date - {initial_payment_date}, ödəniş üslubu - {payment_style}, 2-dəfəyə ilkin ödənişin birincisi.",
                                initial_balance=initial_balance,
                                subsequent_balance=subsequent_balance,
                                office_initial_balance=office_initial_balance,
                                office_subsequent_balance=office_subsequent_balance,
                                executor=user,
                                operation_style="MƏDAXİL",
                                quantity=float(initial_payment)
                            )
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)

                        elif ((nowki_date_san == initial_payment_date_san) and (
                                initial_payment_date_san == initial_payment_debt_date_san)):
                            return Response({
                                "detail": "İlkin ödəniş qalıq və ilkin ödəniş hər ikisi bu günki dateə note oluna bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
                        elif (nowki_date_san == initial_payment_debt_date_san):
                            return Response({"detail": "İlkin ödəniş qalıq bu günki dateə note oluna bilməz"},
                                            status=status.HTTP_400_BAD_REQUEST)
                        elif (initial_payment_date_san > initial_payment_debt_date_san):
                            return Response(
                                {"detail": "İlkin ödəniş qalıq datei ilkin ödəniş dateindən əvvəl ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
                        elif (initial_payment_date_san == initial_payment_debt_date_san):
                            return Response({
                                "detail": "İlkin ödəniş qalıq və ilkin ödəniş hər ikisi eyni dateə note oluna bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
                        elif ((nowki_date_san > initial_payment_date_san) or (
                                nowki_date_san > initial_payment_debt_date_san)):
                            return Response({"detail": "İlkin ödəniş dateini keçmiş dateə təyin edə bilməzsiniz"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        elif (nowki_date_san < initial_payment_date_san):
                            reduce_product_from_stock(stok, int(product_quantity))
                            total_amount = umumi_amount(
                                product.price, int(product_quantity))

                            # remaining_debt = float(total_amount) - float(initial_payment_debt) - float(initial_payment)
                            remaining_debt = float(total_amount)

                            serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company,
                                            office=office, initial_payment=initial_payment,
                                            initial_payment_debt=initial_payment_debt, initial_payment_status="DAVAM EDƏN",
                                            initial_payment_debt_status="DAVAM EDƏN",
                                            total_amount=total_amount, remaining_debt=remaining_debt)
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)
                        elif ((nowki_date_san < initial_payment_date_san) and (
                                nowki_date_san < initial_payment_debt_date_san)):
                            reduce_product_from_stock(stok, int(product_quantity))
                            total_amount = umumi_amount(
                                product.price, int(product_quantity))

                            # remaining_debt = float(total_amount) - float(initial_payment_debt) - float(initial_payment)
                            remaining_debt = float(total_amount)

                            serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company,
                                            office=office, initial_payment=initial_payment,
                                            initial_payment_debt=initial_payment_debt, initial_payment_status="DAVAM EDƏN",
                                            initial_payment_debt_status="DAVAM EDƏN",
                                            total_amount=total_amount, remaining_debt=remaining_debt)
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)

                        # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                        #                 status=status.HTTP_201_CREATED)
                        return Response(data=serializer.data,
                                        status=status.HTTP_201_CREATED)
                    else:
                        return Response({"detail": "Qalıq ilkin ödəniş doğru daxil edilməyib."},
                                        status=status.HTTP_400_BAD_REQUEST)

            # Negd odenis
            elif (payment_style == "NƏĞD"):
                if (loan_term is not None):
                    return Response({"detail": "Kredit müddəti ancaq status installment olan müqavilələr üçündür"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if (initial_payment is not None or initial_payment_debt is not None):
                    return Response({"detail": "İlkin ödəniş ancaq status installment olan müqavilələr üçündür"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if (product_quantity == None):
                    product_quantity = 1

                reduce_product_from_stock(stok, int(product_quantity))
                total_amount = umumi_amount(
                    product.price, int(product_quantity))

                initial_balance = holding_umumi_balance_hesabla()
                office_initial_balance = office_balance_hesabla(office=office)

                note = f"GroupLeader - {user.fullname}, müştəri - {customer.fullname}, date - {nowki_date_date}, ödəniş üslubu - {payment_style}"
                c_income(cashbox, float(total_amount), user, note)

                serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company, office=office,
                                contract_status="BİTMİŞ", total_amount=total_amount)

                subsequent_balance = holding_umumi_balance_hesabla()
                office_subsequent_balance = office_balance_hesabla(office=office)
                pul_axini_create(
                    office=office,
                    company=office.company,
                    description=note,
                    initial_balance=initial_balance,
                    subsequent_balance=subsequent_balance,
                    office_initial_balance=office_initial_balance,
                    office_subsequent_balance=office_subsequent_balance,
                    executor=user,
                    operation_style="MƏDAXİL",
                    quantity=float(total_amount)
                )
                # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"}, status=status.HTTP_201_CREATED)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        traceback.print_exc()
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)

def contract_update(self, request, *args, **kwargs):
    try:
        contract = self.get_object()
        serializer = self.get_serializer(contract, data=request.data, partial=True)
        # serializer = ContractSerializer(contract, data=request.data, partial=True)
        initial_payment = contract.initial_payment
        initial_payment_debt = contract.initial_payment_debt
        initial_payment_status = contract.initial_payment_status
        initial_payment_debt_status = contract.initial_payment_debt_status
        odemek_istediyi_initial_payment = request.data.get("initial_payment")
        odemek_istediyi_qaliq_initial_payment = request.data.get(
            "initial_payment_debt")

        contract_status = contract.contract_status
        my_time = datetime.datetime.min.time()

        nowki_date_date = datetime.date.today()
        nowki_date = datetime.datetime.combine(nowki_date_date, my_time)
        nowki_date_san = datetime.datetime.timestamp(nowki_date)
        dusen_contract_status = request.data.get("contract_status")
        product = contract.product
        product_quantity = contract.product_quantity
        contract_group_leader = contract.group_leader
        office=contract.office
        customer = contract.customer
        customer_id = request.data.get("customer_id")
        if (customer_id is not None):
            customer = get_object_or_404(Customer, pk=customer_id)

        contract_manager1 = contract.manager1
        yeni_qrafik = request.data.get("new_graphic_status")
        # YENI QRAFIK ile bagli operationlar
        if(yeni_qrafik == "YENİ QRAFİK"):
            initial_payment = contract.initial_payment
            initial_payment_debt = contract.initial_payment_debt
            initial_payment_tam = initial_payment + initial_payment_debt
            productun_pricei = contract.total_amount
            odenen_installmentler = Installment.objects.filter(
                contract=contract, payment_status="ÖDƏNƏN")

            odenmeyen_installmentler = Installment.objects.filter(
                contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)

            sertli_odeme = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN").exclude(conditional_payment_status=None)

            odenmeyen_installmenti_amount = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)[0].price

            odemek_istediyi_amount = float(
                request.data.get("new_graphic_amount"))

            if odemek_istediyi_amount < odenmeyen_installmenti_amount:
                odenen_amount = 0
                for i in odenen_installmentler:
                    odenen_amount += float(i.price)

                sertli_odemeden_gelen_amount = 0
                for s in sertli_odeme:
                    sertli_odemeden_gelen_amount += float(s.price)
                odediyi = float(odenen_amount) + initial_payment_tam
                remaining_debt = productun_pricei - odediyi
                cixilacaq_amount = remaining_debt -  sertli_odemeden_gelen_amount

                odenmeyen_aylar = len(odenmeyen_installmentler)
                try:
                    elave_olunacaq_ay_qaliqli = cixilacaq_amount / odemek_istediyi_amount
                    # contract.new_graphic_status = "YENİ QRAFİK"
                    contract.remaining_debt = remaining_debt
                    contract.save()
                except:
                    return Response({"detail": "Ödəmək istədiyiniz məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

                elave_olunacaq_ay = math.ceil(elave_olunacaq_ay_qaliqli)
                create_olunacaq_ay = elave_olunacaq_ay - len(odenmeyen_installmentler)
                a = odemek_istediyi_amount * (elave_olunacaq_ay-1)
                son_aya_elave_edilecek_amount = cixilacaq_amount - a
                inc_month = pd.date_range(odenmeyen_installmentler[len(
                    odenmeyen_installmentler)-1].date, periods=create_olunacaq_ay+1, freq='M')

                contract.loan_term = contract.loan_term + create_olunacaq_ay
                contract.save()
                # Var olan aylarin priceini customernin istediyi price edir
                i = 0
                while(i < len(odenmeyen_installmentler)):
                    odenmeyen_installmentler[i].price = odemek_istediyi_amount
                    odenmeyen_installmentler[i].save()
                    i += 1
                # Elave olunacaq aylari create edir
                o_t = Installment.objects.filter(contract=contract)
                c = int(list(o_t)[-1].month_no) + 1
                j = 1
                while(j <= create_olunacaq_ay):
                    if(j == create_olunacaq_ay):
                        if(datetime.date.today().day < 29):
                            Installment.objects.create(
                                month_no=c,
                                contract=contract,
                                date=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                price=son_aya_elave_edilecek_amount,
                                last_month=True
                            ).save()
                        elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                            if(inc_month[j].day <= datetime.date.today().day):
                                Installment.objects.create(
                                    month_no=c,
                                    contract=contract,
                                    date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}",
                                    price=son_aya_elave_edilecek_amount,
                                    last_month=True
                                ).save()
                            else:
                                Installment.objects.create(
                                    month_no=c,
                                    contract=contract,
                                    date=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                    price=son_aya_elave_edilecek_amount,
                                    last_month=True
                                ).save()
                    else:
                        if(datetime.date.today().day < 29):
                            Installment.objects.create(
                                month_no=c,
                                contract=contract,
                                date=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                price=odemek_istediyi_amount
                            ).save()
                        elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                            if(inc_month[j].day <= datetime.date.today().day):
                                Installment.objects.create(
                                    month_no=c,
                                    contract=contract,
                                    date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}",
                                    price=odemek_istediyi_amount
                                ).save()
                            else:
                                Installment.objects.create(
                                    month_no=c,
                                    contract=contract,
                                    date=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                    price=odemek_istediyi_amount
                                ).save()
                    c+=1
                    j+= 1
                    
                pdf_create_when_contract_updated(
                    sender=contract, instance=contract, created=True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Məbləğ cari məbləğdən artıq ola bilməz!"}, status=status.HTTP_400_BAD_REQUEST)
        if (contract.contract_status == "DÜŞƏN" and request.data.get("contract_status") == "DAVAM EDƏN"):
            """
            Müqavilə düşən statusundan davam edən statusuna qaytarılarkən bu hissə işə düşür
            """
            contract.contract_status = "DAVAM EDƏN"
            contract.is_remove = False
            contract.save()

            try:
                warehouse = get_object_or_404(Warehouse, office=contract.office)
            except:
                return Response({"detail": "Warehouse tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                stok = get_object_or_404(Stock, warehouse=warehouse, product=product)
            except:
                return Response({"detail": "Warehouseın stokunda məhsul yoxdur"}, status=status.HTTP_400_BAD_REQUEST)

            if (stok.quantity < int(product_quantity)):
                return Response({"detail": "Stockda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

            reduce_product_from_stock(stok, product_quantity)

            contract_date = contract.contract_date
            year = contract_date.year
            month = contract_date.month
            date = datetime.date(year=year, month=month, day=1)
            odenmeyen_installmentler_qs = Installment.objects.filter(
                contract=contract, payment_status="ÖDƏNMƏYƏN")
            odenmeyen_installmentler = list(odenmeyen_installmentler_qs)
            now = datetime.datetime.today().strftime('%d-%m-%Y')
            inc_month = pd.date_range(now, periods=len(
                odenmeyen_installmentler), freq='M')
            i = 0
            while (i < len(odenmeyen_installmentler)):
                if (datetime.date.today().day < 29):
                    odenmeyen_installmentler[
                        i].date = f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}"
                    odenmeyen_installmentler[i].save()
                elif (
                        datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                    odenmeyen_installmentler[i].date = f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                    odenmeyen_installmentler[i].save()
                i += 1

            create_services(contract, contract, True)

            return Response({"detail": "Müqavilə düşən statusundan davam edən statusuna keçirildi"},
                            status=status.HTTP_200_OK)

        if (contract.contract_status == "DAVAM EDƏN" and request.data.get("contract_status") == "DÜŞƏN"):
            """
            Müqavilə düşən statusuna keçərkən bu hissə işə düşür
            """
            contract_date = contract.contract_date
            year = contract_date.year
            month = contract_date.month
            date = datetime.date(year=year, month=month, day=1)
            compensation_income = request.data.get("compensation_income")
            compensation_expense = request.data.get("compensation_expense")

            contract_group_leader = contract.group_leader
            contract_manager1 = contract.manager1

            cashbox = get_object_or_404(OfficeCashbox, office=contract.office)
            cashbox_balance = cashbox.balance
            if (compensation_income is not None and compensation_expense is not None):
                return Response({"detail": "Kompensasiya məxaric və mədaxil eyni anda edilə bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)

            if (compensation_income is not None):
                initial_balance = holding_umumi_balance_hesabla()
                office_initial_balance = office_balance_hesabla(office=office)

                user = request.user
                customer = contract.customer

                note = f"GroupLeader - {contract_group_leader.fullname}, müştəri - {customer.fullname}, date - {nowki_date_date}, müqavilə düşən statusuna keçirildiyi üçün. Kompensasiya məbləği => {compensation_income}"
                c_income(cashbox, float(compensation_income),
                          contract_group_leader, note)

                contract.contract_status = "DÜŞƏN"
                contract.compensation_income = request.data.get("compensation_income")
                contract.save()
                
                subsequent_balance = holding_umumi_balance_hesabla()
                office_subsequent_balance = office_balance_hesabla(office=office)
                pul_axini_create(
                    office=contract.office,
                    company=contract.office.company,
                    description=note,
                    initial_balance=initial_balance,
                    subsequent_balance=subsequent_balance,
                    office_initial_balance=office_initial_balance,
                    office_subsequent_balance=office_subsequent_balance,
                    executor=user,
                    operation_style="MƏDAXİL",
                    quantity=float(compensation_income)
                )


            elif (compensation_expense is not None):
                if (cashbox_balance < float(compensation_expense)):
                    return Response({"detail": "Kompensasiya məxaric məbləği Officein balanceından çox ola bilməz"},
                                    status=status.HTTP_400_BAD_REQUEST)
                initial_balance = holding_umumi_balance_hesabla()
                office_initial_balance = office_balance_hesabla(office=office)

                user = request.user
                customer = contract.customer

                note = f"GroupLeader - {contract_group_leader.fullname}, müştəri - {customer.fullname}, date - {nowki_date_date}, müqavilə düşən statusuna keçirildiyi üçün. Kompensasiya məbləği => {compensation_expense}"
                expense(cashbox, float(compensation_expense),
                          contract_group_leader, note)

                contract.contract_status = "DÜŞƏN"
                contract.compensation_expense = request.data.get("compensation_expense")
                contract.save()

                subsequent_balance = holding_umumi_balance_hesabla()
                office_subsequent_balance = office_balance_hesabla(office=office)
                pul_axini_create(
                    office=contract.office,
                    company=contract.office.company,
                    description=note,
                    initial_balance=initial_balance,
                    subsequent_balance=subsequent_balance,
                    office_initial_balance=office_initial_balance,
                    office_subsequent_balance=office_subsequent_balance,
                    executor=user,
                    operation_style="MƏXARİC",
                    quantity=float(compensation_expense)
                )

            if (compensation_income == "" and compensation_expense == ""):
                contract.contract_status = "DÜŞƏN"
                contract.save()

            contract_group_leader = contract.group_leader
            contract_manager1 = contract.manager1

            try:
                warehouse = get_object_or_404(Warehouse, office=contract.office)
            except:
                return Response({"detail": "Warehouse tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

            stok = get_object_or_404(Stock, warehouse=warehouse, product=product)
            add_product_to_stock(stok, product_quantity)

            now = datetime.date.today()
            d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
            next_m = d + pd.offsets.MonthBegin(1)

            all_service = Service.objects.filter(contract=contract)
            for service in all_service:
                all_service_payment = ServicePayment.objects.filter(
                    service=service, is_done=False)
                if len(all_service_payment) == 1:
                    all_service_payment[0].delete()
                else:
                    for service_payment in all_service_payment:
                        service_payment.delete()
                service.delete()

            # -------------------- Maaslarin geri qaytarilmasi --------------------
            contract_payment_style = contract.payment_style
            group_leader = contract.group_leader
            contract_loan_term = contract.loan_term

            try:
                name = group_leader.position.name
            except:
                name = None

            if name == "VANLEADER":
                if group_leader is not None:
                    group_leader_status = group_leader.employee_status
                    try:
                        group_leader_position = group_leader.position.name
                    except:
                        group_leader_position = None
                    if (group_leader_status is not None):
                        group_leader_prim = GroupLeaderPrimNew.objects.get(
                            prim_status=group_leader_status, position=group_leader.position)
                        group_leader_mg_nowki_ay = SalaryView.objects.get(
                            employee=contract_group_leader, date=f"{now.year}-{now.month}-{1}")
                        group_leader_mg_novbeti_ay = SalaryView.objects.get(
                            employee=contract_group_leader, date=next_m)

                        group_leader_mg_nowki_ay.sale_quantity = float(
                            group_leader_mg_nowki_ay.sale_quantity) - float(product_quantity)
                        group_leader_mg_nowki_ay.sales_amount = float(
                            group_leader_mg_nowki_ay.sales_amount) - (float(contract.product.price) * float(contract.product_quantity))

                        # group_leader_mg_novbeti_ay.final_salary = float(group_leader_mg_novbeti_ay.final_salary) - float(group_leader_prim.prim_for_team)

                        if contract_payment_style == "NƏĞD":
                            group_leader_mg_novbeti_ay.final_salary = float(
                                group_leader_mg_novbeti_ay.final_salary) - (float(group_leader_prim.cash) * float(contract.product_quantity))
                        elif contract_payment_style == "KREDİT":
                            if int(contract_loan_term) >= 0 and int(contract_loan_term) <= 3:
                                group_leader_mg_novbeti_ay.final_salary = float(
                                    group_leader_mg_novbeti_ay.final_salary) - (float(group_leader_prim.cash) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 4 and int(contract_loan_term) <= 12:
                                group_leader_mg_novbeti_ay.final_salary = float(group_leader_mg_novbeti_ay.final_salary) - (
                                    float(group_leader_prim.installment_4_12) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 13 and int(contract_loan_term) <= 18:
                                group_leader_mg_novbeti_ay.final_salary = float(group_leader_mg_novbeti_ay.final_salary) - (
                                    float(group_leader_prim.installment_13_18) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 19 and int(contract_loan_term) <= 24:
                                group_leader_mg_novbeti_ay.final_salary = float(group_leader_mg_novbeti_ay.final_salary) - (
                                    float(group_leader_prim.installment_19_24) * float(contract.product_quantity))

                        group_leader_mg_nowki_ay.save()
                        group_leader_mg_novbeti_ay.save()

                manager1 = contract.manager1
                if manager1 is not None:
                    manager1_status = manager1.employee_status
                    try:
                        manager1_position = manager1.position.name
                    except:
                        manager1_position = None
                    if (manager1_position == "DEALER"):
                        manager1_prim = Manager1PrimNew.objects.get(
                            prim_status=manager1_status, position=manager1.position)
                        manager1_mg_nowki_ay = SalaryView.objects.get(
                            employee=contract_manager1, date=f"{now.year}-{now.month}-{1}")
                        manager1_mg_novbeti_ay = SalaryView.objects.get(
                            employee=contract_manager1, date=next_m)

                        manager1_mg_nowki_ay.sale_quantity = float(
                            manager1_mg_nowki_ay.sale_quantity) - float(product_quantity)
                        manager1_mg_nowki_ay.sales_amount = float(manager1_mg_nowki_ay.sales_amount) - (
                            float(contract.product.price) * float(contract.product_quantity))

                        if contract_payment_style == "NƏĞD":
                            manager1_mg_novbeti_ay.final_salary = float(
                                manager1_mg_novbeti_ay.final_salary) - (float(manager1_prim.cash) * float(contract.product_quantity))
                        elif contract_payment_style == "KREDİT":
                            if int(contract_loan_term) >= 0 and int(contract_loan_term) <= 3:
                                manager1_mg_novbeti_ay.final_salary = float(
                                    manager1_mg_novbeti_ay.final_salary) - (float(manager1_prim.cash) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 4 and int(contract_loan_term) <= 12:
                                manager1_mg_novbeti_ay.final_salary = float(manager1_mg_novbeti_ay.final_salary) - (
                                    float(manager1_prim.installment_4_12) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 13 and int(contract_loan_term) <= 18:
                                manager1_mg_novbeti_ay.final_salary = float(manager1_mg_novbeti_ay.final_salary) - (
                                    float(manager1_prim.installment_13_18) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 19 and int(contract_loan_term) <= 24:
                                manager1_mg_novbeti_ay.final_salary = float(manager1_mg_novbeti_ay.final_salary) - (
                                    float(manager1_prim.installment_19_24) * float(contract.product_quantity))

                        manager1_mg_nowki_ay.save()
                        manager1_mg_novbeti_ay.save()

                office = contract.office
                if office is not None:
                    officeLeaderPosition = Position.objects.get(
                        name="OFFICE LEADER", company=contract.company)
                    officeLeaders = User.objects.filter(
                        office=office, position=officeLeaderPosition)
                    for officeLeader in officeLeaders:
                        officeLeader_status = officeLeader.employee_status
                        officeleader_prim = OfficeLeaderPrim.objects.get(
                            prim_status=officeLeader_status, position=officeLeader.position)

                        officeLeader_salary_view_this_month = SalaryView.objects.get(
                            employee=officeLeader, date=f"{now.year}-{now.month}-{1}")
                        officeLeader_salary_goruntulenme_novbeti_ay = SalaryView.objects.get(
                            employee=officeLeader, date=next_m)

                        officeLeader_salary_view_this_month.sale_quantity = float(
                            officeLeader_salary_view_this_month.sale_quantity) - float(product_quantity)
                        officeLeader_salary_view_this_month.sales_amount = float(officeLeader_salary_view_this_month.sales_amount) - (float(contract.product.price) * float(contract.product_quantity))
                        officeLeader_salary_view_this_month.save()

                        officeLeader_salary_goruntulenme_novbeti_ay.final_salary = float(
                            officeLeader_salary_goruntulenme_novbeti_ay.final_salary) - (float(officeleader_prim.prim_for_office) * float(contract.product_quantity))
                        officeLeader_salary_goruntulenme_novbeti_ay.save()
            
            # -------------------- -------------------- --------------------
            contract.cancelled_date = datetime.date.today()
            contract.contract_status = "DÜŞƏN"
            contract.is_remove = True
            contract.save()
            
            return Response({"detail": "Müqavilə düşən statusuna keçirildi"}, status=status.HTTP_200_OK)

        if (contract.payment_style == "KREDİT"):
            if (odemek_istediyi_initial_payment != None and initial_payment_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_initial_payment) != initial_payment):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
                elif (float(odemek_istediyi_initial_payment) == initial_payment):
                    contract.initial_payment_status = "BİTMİŞ"
                    contract.initial_payment_date = nowki_date_date
                    contract.remaining_debt = float(
                        contract.remaining_debt) - float(initial_payment)
                    contract.save()
                    return Response({"detail": "İlkin ödəniş ödənildi"}, status=status.HTTP_200_OK)

            if (odemek_istediyi_qaliq_initial_payment != None and initial_payment_status == "BİTMİŞ" and initial_payment_debt_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_qaliq_initial_payment) == initial_payment_debt):
                    contract.initial_payment_debt_status = "BİTMİŞ"
                    contract.initial_payment_debt_date = nowki_date_date
                    contract.remaining_debt = float(
                        contract.remaining_debt) - float(initial_payment_debt)
                    contract.save()
                    return Response({"detail": "Qalıq ilkin ödəniş ödənildi"}, status=status.HTTP_200_OK)
                elif (float(odemek_istediyi_qaliq_initial_payment) != initial_payment_debt):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "Bu əməliyyatı icra etmək mümkün olmadı"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception:
        traceback.print_exc()
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)
