import datetime
import math
from typing import Optional
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from account.models import Customer
from company.models import Company, Office, Position
from cashbox.models import OfficeCashbox
from salary.models import (
    Manager1PrimNew, 
    SalaryView, 
    OfficeLeaderPrim, 
    GroupLeaderPrimNew
)
from contract.models import Contract, Installment
from warehouse.models import (
    Warehouse,
    Stock
)
from product.models import Product
from services.models import Service, ServicePayment
from rest_framework.generics import get_object_or_404
import pandas as pd
from datetime import date
import traceback
from services.signals import create_services

from api.v1.cashbox.utils import (
    calculate_holding_total_balance, 
    cashflow_create, 
    calculate_office_balance, 
)

from django.contrib.auth import get_user_model

from api.v1.contract.utils.contract_utils import (
    add_product_to_stock,
    c_income,
    calculate_holding_total_balance,
    calculate_office_balance,
    cashflow_create,
    expense,
    pdf_create_when_contract_updated,
    reduce_product_from_stock,   
)

from contract import CASH, NEW_GRAPH, CONTINUING, INSTALLMENT, CANCELLED

User = get_user_model()

# -------------------------------------------

def total_amount(product_price, product_quantity):
    total_amount = product_price * product_quantity
    return total_amount

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
        return Response({"detail": "Müştəri qeyd olunmayıb"}, status=status.HTTP_400_BAD_REQUEST)
    customer = get_object_or_404(Customer, pk=customer_id)

    manager1 = None
    manager2 = None

    if (manager1_id is not None):
        try:
            manager1 = get_object_or_404(User, pk=manager1_id)
            if (manager2_id == None):
                manager2 = manager1
        except:
            return Response({"detail": "Menecer 1 tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    if (manager2_id is not None):
        try:
            manager2 = get_object_or_404(User, pk=manager2_id)
            if (manager1_id == None):
                manager1 = manager2
        except:
            return Response({"detail": "Menecer 2 tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    my_time = datetime.datetime.min.time()

    now_date_date = datetime.date.today()
    now_date = datetime.datetime.combine(now_date_date, my_time)
    now_date_san = datetime.datetime.timestamp(now_date)

    if (request.data.get("initial_payment_date") is not None):
        initial_payment_date = request.data.get("initial_payment_date")
        initial_payment_date_date = datetime.datetime.strptime(initial_payment_date, "%d-%m-%Y")
        initial_payment_date_san = datetime.datetime.timestamp(initial_payment_date_date)

    if (request.data.get("initial_payment_debt_date") is not None):
        initial_payment_debt_date = request.data.get("initial_payment_debt_date")
        initial_payment_debt_date_date = datetime.datetime.strptime(initial_payment_debt_date, "%d-%m-%Y")
        initial_payment_debt_date_san = datetime.datetime.timestamp(initial_payment_debt_date_date)

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

    def calc_total_amount(product_price, product_quantity):
        total_amount = product_price * product_quantity
        return total_amount

    if (product_quantity == None):
        product_quantity = 1

    total_amount = calc_total_amount(product.price, int(product_quantity))

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
        return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cashbox = get_object_or_404(OfficeCashbox, office=office)
    except:
        traceback.print_exc()
        return Response({"detail": "Ofis Kassa tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    cashbox_balance = cashbox.balance
    remaining_debt = 0

    try:
        try:
            stok = get_object_or_404(Stock, warehouse=warehouse, product=product)
        except:
            return Response({"detail": "Stokda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)
        if (stok.quantity < int(product_quantity)):
            return Response({"detail": "Stokda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

        if (serializer.is_valid()):
            if (product_quantity == None):
                product_quantity = 1
            # Kredit
            if (payment_style == INSTALLMENT):
                if (loan_term == None):
                    # Kredit muddeti daxil edilmezse
                    return Response({"detail": "Ödəmə statusu kreditdir amma kredit müddəti daxil edilməyib"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif (int(loan_term) == 0):
                    # Kredit muddeyi 0 daxil edilerse
                    return Response({"detail": "Ödəmə statusu kreditdir amma kredit müddəti 0 daxil edilib"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif (int(loan_term) > 30):
                    # Kredit muddeti 31 ay daxil edilerse
                    return Response({"detail": "Maksimum kredit müddəti 30 aydır"}, status=status.HTTP_400_BAD_REQUEST)
                elif (int(loan_term) > 0):
                    # Kredit muddeti 0-dan boyuk olarsa

                    if ((initial_payment is not None) and (request.data.get("initial_payment_date") == None)):
                        initial_payment_date = now_date_date
                        initial_payment_date_date = now_date
                        initial_payment_date_san = now_date_san

                    if ((initial_payment_debt is not None) and (request.data.get("initial_payment_debt_date") == None)):
                        return Response({
                            "detail": "Qalıq İlkin ödəniş məbləği qeyd olunub amma qalıq ilkin ödəniş tarixi qeyd olunmayıb"},
                            status=status.HTTP_400_BAD_REQUEST)

                    if (initial_payment == None and initial_payment_debt == None):
                        # Ilkin odenis daxil edilmezse
                        reduce_product_from_stock(stok, int(product_quantity))
                        total_amount = calc_total_amount(
                            product.price, int(product_quantity))

                        remaining_debt = float(total_amount)

                        serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company, office=office,
                                        total_amount=total_amount, remaining_debt=remaining_debt)
                        return Response(data=serializer.data,
                                        status=status.HTTP_201_CREATED)
                    elif (initial_payment is not None and initial_payment_debt == None):
                        total_amount = calc_total_amount(product.price, int(product_quantity))
                        if float(initial_payment) >= float(total_amount):
                            return Response({"detail": "İlkin ödəniş məbləği müqavilənin məbləğindən çox ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
                        # ilkin odenis bu gunku tarixe daxil edilerse ve qaliq ilkin odenis daxil edilmezse
                        if (now_date_san == initial_payment_date_san):
                            reduce_product_from_stock(stok, int(product_quantity))
                            total_amount = calc_total_amount(product.price, int(product_quantity))
                            
                            initial_balance = calculate_holding_total_balance()
                            office_initial_balance = calculate_office_balance(office=office)
                            note = f"GroupLeader - {user.fullname}, müştəri - {customer.fullname}, tarix - {initial_payment_date}, ödəniş üslubu - {payment_style}, tam ilkin ödəniş"
                            c_income(cashbox, float(
                                initial_payment), user, note)

                            remaining_debt = float(
                                total_amount) - float(initial_payment)
                            serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company,
                                            office=office, initial_payment=initial_payment,
                                            initial_payment_status="BİTMİŞ", total_amount=total_amount, remaining_debt=remaining_debt,)
                            subsequent_balance = calculate_holding_total_balance()
                            office_subsequent_balance = calculate_office_balance(office=office)
                            cashflow_create(
                                office=office,
                                company=office.company,
                                description=f"GroupLeader - {user.fullname}, müştəri - {customer.fullname}, tarix - {initial_payment_date}, ödəniş üslubu - {payment_style}, tam ilkin ödəniş",
                                initial_balance=initial_balance,
                                subsequent_balance=subsequent_balance,
                                office_initial_balance=office_initial_balance,
                                office_subsequent_balance=office_subsequent_balance,
                                executor=user,
                                operation_style="MƏDAXİL",
                                quantity=float(initial_payment)
                            )
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)
                        elif (now_date_san < initial_payment_date_san):
                            reduce_product_from_stock(stok, int(product_quantity))
                            total_amount = calc_total_amount(
                                product.price, int(product_quantity))

                            # remaining_debt = float(total_amount) - float(initial_payment)
                            remaining_debt = float(total_amount)

                            serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company,
                                            office=office, initial_payment=initial_payment,
                                            initial_payment_status=CONTINUING, remaining_debt=remaining_debt,
                                            total_amount=total_amount)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)
                        elif (now_date_san > initial_payment_date_san):
                            return Response({"detail": "İlkin ödəniş tarixini keçmiş tarixə təyin edə bilməzsiniz"},
                                            status=status.HTTP_400_BAD_REQUEST)
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
                        total_amount2 = calc_total_amount(product.price, int(product_quantity))
                        remaining_debt2 = float(total_amount2) - float(initial_payment_debt)
                        if float(initial_payment) >= float(remaining_debt2):
                            return Response({"detail": "İlkin ödəniş qalıq məbləği qalıq məbləğdən çox ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
                        if ((now_date_san == initial_payment_date_san) and (
                                now_date_san < initial_payment_debt_date_san)):
                            reduce_product_from_stock(stok, int(product_quantity))
                            total_amount = calc_total_amount(
                                product.price, int(product_quantity))

                            initial_balance = calculate_holding_total_balance()
                            office_initial_balance = calculate_office_balance(office=office)

                            note = f"GroupLeader - {user.fullname}, müştəri - {customer.fullname}, tarix - {initial_payment_date}, ödəniş üslubu - {payment_style}, 2-dəfəyə ilkin ödənişin birincisi."
                            c_income(cashbox, float(
                                initial_payment), user, note)

                            remaining_debt = float(total_amount) - float(initial_payment)

                            serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company,
                                            office=office, initial_payment=initial_payment,
                                            initial_payment_debt=initial_payment_debt, initial_payment_status="BİTMİŞ",
                                            initial_payment_debt_status=CONTINUING,
                                            total_amount=total_amount, remaining_debt=remaining_debt)
                            subsequent_balance = calculate_holding_total_balance()
                            office_subsequent_balance = calculate_office_balance(office=office)
                            cashflow_create(
                                office=office,
                                company=office.company,
                                description=f"GroupLeader - {user.fullname}, müştəri - {customer.fullname}, tarix - {initial_payment_date}, ödəniş üslubu - {payment_style}, 2-dəfəyə ilkin ödənişin birincisi.",
                                initial_balance=initial_balance,
                                subsequent_balance=subsequent_balance,
                                office_initial_balance=office_initial_balance,
                                office_subsequent_balance=office_subsequent_balance,
                                executor=user,
                                operation_style="MƏDAXİL",
                                quantity=float(initial_payment)
                            )
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)

                        elif ((now_date_san == initial_payment_date_san) and (
                                initial_payment_date_san == initial_payment_debt_date_san)):
                            return Response({
                                "detail": "İlkin ödəniş qalıq və ilkin ödəniş hər ikisi bu günki tarixə qeyd oluna bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
                        elif (now_date_san == initial_payment_debt_date_san):
                            return Response({"detail": "İlkin ödəniş qalıq bu günki tarixə qeyd oluna bilməz"},
                                            status=status.HTTP_400_BAD_REQUEST)
                        elif (initial_payment_date_san > initial_payment_debt_date_san):
                            return Response(
                                {"detail": "İlkin ödəniş qalıq tarixi ilkin ödəniş tarixindən əvvəl ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
                        elif (initial_payment_date_san == initial_payment_debt_date_san):
                            return Response({
                                "detail": "İlkin ödəniş qalıq və ilkin ödəniş hər ikisi eyni tarixə qeyd oluna bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
                        elif ((now_date_san > initial_payment_date_san) or (
                                now_date_san > initial_payment_debt_date_san)):
                            return Response({"detail": "İlkin ödəniş dateini keçmiş tarixə təyin edə bilməzsiniz"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        elif (now_date_san < initial_payment_date_san):
                            reduce_product_from_stock(stok, int(product_quantity))
                            total_amount = calc_total_amount(
                                product.price, int(product_quantity))

                            remaining_debt = float(total_amount)

                            serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company,
                                            office=office, initial_payment=initial_payment,
                                            initial_payment_debt=initial_payment_debt, initial_payment_status=CONTINUING,
                                            initial_payment_debt_status=CONTINUING,
                                            total_amount=total_amount, remaining_debt=remaining_debt)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)
                        elif ((now_date_san < initial_payment_date_san) and (
                                now_date_san < initial_payment_debt_date_san)):
                            reduce_product_from_stock(stok, int(product_quantity))
                            total_amount = calc_total_amount(
                                product.price, int(product_quantity))

                            remaining_debt = float(total_amount)

                            serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company,
                                            office=office, initial_payment=initial_payment,
                                            initial_payment_debt=initial_payment_debt, initial_payment_status=CONTINUING,
                                            initial_payment_debt_status=CONTINUING,
                                            total_amount=total_amount, remaining_debt=remaining_debt)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)

                        return Response(data=serializer.data,
                                        status=status.HTTP_201_CREATED)
                    else:
                        return Response({"detail": "Qalıq ilkin ödəniş doğru daxil edilməyib."},
                                        status=status.HTTP_400_BAD_REQUEST)

            # Negd odenis
            elif (payment_style == CASH):
                if (loan_term is not None):
                    return Response({"detail": "Kredit müddəti ancaq status kredit olan müqavilələr üçündür"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if (initial_payment is not None or initial_payment_debt is not None):
                    return Response({"detail": "İlkin ödəniş ancaq status kredit olan müqavilələr üçündür"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if (product_quantity == None):
                    product_quantity = 1

                reduce_product_from_stock(stok, int(product_quantity))
                total_amount = calc_total_amount(
                    product.price, int(product_quantity))

                initial_balance = calculate_holding_total_balance()
                office_initial_balance = calculate_office_balance(office=office)

                note = f"GroupLeader - {user.fullname}, müştəri - {customer.fullname}, date - {now_date_date}, ödəniş üslubu - {payment_style}"
                c_income(cashbox, float(total_amount), user, note)

                serializer.save(group_leader=user, manager1=manager1, manager2=manager2, company=company, office=office,
                                contract_status="BİTMİŞ", total_amount=total_amount)

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
                    operation_style="MƏDAXİL",
                    quantity=float(total_amount)
                )
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
        initial_payment = contract.initial_payment
        initial_payment_debt = contract.initial_payment_debt
        initial_payment_status = contract.initial_payment_status
        initial_payment_debt_status = contract.initial_payment_debt_status
        wants_to_pay_initial_payment = request.data.get("initial_payment")
        wants_to_pay_debt_initial_payment = request.data.get("initial_payment_debt")

        now_date_date = datetime.date.today()
        product = contract.product
        product_quantity = contract.product_quantity
        contract_group_leader = contract.group_leader
        office=contract.office
        customer = contract.customer
        customer_id = request.data.get("customer_id")
        if (customer_id is not None):
            customer = get_object_or_404(Customer, pk=customer_id)

        contract_manager1 = contract.manager1
        new_graphic = request.data.get("new_graphic_status")
        # YENI QRAFIK ile bagli əməliyyatlar
        if(new_graphic == NEW_GRAPH):
            initial_payment = contract.initial_payment
            initial_payment_debt = contract.initial_payment_debt
            initial_payment_total = initial_payment + initial_payment_debt
            product_price = contract.total_amount
            installments_paid = Installment.objects.filter(contract=contract, payment_status="ÖDƏNƏN")

            unpaid_installments = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)

            conditional_payment = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN").exclude(conditional_payment_status=None)

            unpaid_installments_amount = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN", conditional_payment_status=None)[0].price

            wants_to_pay_amount = float(request.data.get("new_graphic_amount"))

            if wants_to_pay_amount < unpaid_installments_amount:
                paid_amount = 0
                for i in installments_paid:
                    paid_amount += float(i.price)

                amount_come_from_conditional_payment = 0
                for s in conditional_payment:
                    amount_come_from_conditional_payment += float(s.price)
                paid = float(paid_amount) + initial_payment_total
                remaining_debt = product_price - paid
                deducted_amount = remaining_debt -  amount_come_from_conditional_payment

                try:
                    added_month_debt = deducted_amount / wants_to_pay_amount
                    contract.new_graphic_amount = wants_to_pay_amount
                    contract.new_graphic_status = NEW_GRAPH
                    contract.save()
                except:
                    return Response({"detail": "Ödəmək istədiyiniz məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

                added_month = math.ceil(added_month_debt)
                month_to_be_created = added_month - len(unpaid_installments)
                a = wants_to_pay_amount * (added_month-1)
                added_amount_to_last_month = deducted_amount - a
                inc_month = pd.date_range(unpaid_installments[len(
                    unpaid_installments)-1].date, periods=month_to_be_created+1, freq='M')

                contract.loan_term = contract.loan_term + month_to_be_created
                contract.save()
                # Var olan aylarin qiymetini musterinin istediyi qiymet edir
                i = 0
                while(i < len(unpaid_installments)):
                    unpaid_installments[i].price = wants_to_pay_amount
                    unpaid_installments[i].save()
                    i += 1
                # Elave olunacaq aylari create edir
                instlmnt = Installment.objects.filter(contract=contract)
                month_num = int(list(instlmnt)[-1].month_no) + 1
                j = 1
                while(j <= month_to_be_created):
                    if(j == month_to_be_created):
                        if(datetime.date.today().day < 29):
                            Installment.objects.create(
                                month_no=month_num,
                                contract=contract,
                                date=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                price=added_amount_to_last_month,
                                last_month=True
                            ).save()
                        elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                            if(inc_month[j].day <= datetime.date.today().day):
                                Installment.objects.create(
                                    month_no=month_num,
                                    contract=contract,
                                    date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}",
                                    price=added_amount_to_last_month,
                                    last_month=True
                                ).save()
                            else:
                                Installment.objects.create(
                                    month_no=month_num,
                                    contract=contract,
                                    date=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                    price=added_amount_to_last_month,
                                    last_month=True
                                ).save()
                    else:
                        if(datetime.date.today().day < 29):
                            Installment.objects.create(
                                month_no=month_num,
                                contract=contract,
                                date=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                price=wants_to_pay_amount
                            ).save()
                        elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                            if(inc_month[j].day <= datetime.date.today().day):
                                Installment.objects.create(
                                    month_no=month_num,
                                    contract=contract,
                                    date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}",
                                    price=wants_to_pay_amount
                                ).save()
                            else:
                                Installment.objects.create(
                                    month_no=month_num,
                                    contract=contract,
                                    date=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                    price=wants_to_pay_amount
                                ).save()
                    month_num+=1
                    j+= 1
                    
                pdf_create_when_contract_updated(
                    sender=contract, instance=contract, created=True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Məbləğ cari məbləğdən artıq ola bilməz!"}, status=status.HTTP_400_BAD_REQUEST)
        # Müqavilə düşən statusundan davam edən statusuna qaytarılarkən bu hissə işə düşür
        if (contract.contract_status == CANCELLED and request.data.get("contract_status") == CONTINUING):
            """
            Müqavilə düşən statusundan davam edən statusuna qaytarılarkən bu hissə işə düşür
            """
            contract.contract_status = CONTINUING
            contract.is_remove = False
            contract.save()

            try:
                warehouse = get_object_or_404(Warehouse, office=contract.office)
            except:
                return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                stok = get_object_or_404(Stock, warehouse=warehouse, product=product)
            except:
                return Response({"detail": "Anbarın stokunda məhsul yoxdur"}, status=status.HTTP_400_BAD_REQUEST)

            if (stok.quantity < int(product_quantity)):
                return Response({"detail": "Stokda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

            reduce_product_from_stock(stok, product_quantity)

            contract_date = contract.contract_date
            year = contract_date.year
            month = contract_date.month
            unpaid_installments_qs = Installment.objects.filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
            unpaid_installments = list(unpaid_installments_qs)
            now = datetime.datetime.today().strftime('%d-%m-%Y')
            inc_month = pd.date_range(now, periods=len(
                unpaid_installments), freq='M')
            i = 0
            while (i < len(unpaid_installments)):
                if (datetime.date.today().day < 29):
                    unpaid_installments[
                        i].date = f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}"
                    unpaid_installments[i].save()
                elif (
                        datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                    unpaid_installments[i].date = f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                    unpaid_installments[i].save()
                i += 1

            create_services(contract, contract, True)

            return Response({"detail": "Müqavilə düşən statusundan davam edən statusuna keçirildi"},
                            status=status.HTTP_200_OK)
        # Müqavilə düşən statusuna keçərkən bu hissə işə düşür
        if (contract.contract_status == CONTINUING and request.data.get("contract_status") == CANCELLED):
            """
            Müqavilə düşən statusuna keçərkən bu hissə işə düşür
            """
            contract_date = contract.contract_date
            compensation_income = request.data.get("compensation_income")
            compensation_expense = request.data.get("compensation_expense")
            contract_note = request.data.get("note")

            contract_group_leader = contract.group_leader
            contract_manager1 = contract.manager1

            cashbox = get_object_or_404(OfficeCashbox, office=contract.office)
            cashbox_balance = cashbox.balance
            if (compensation_income is not None and compensation_expense is not None):
                return Response({"detail": "Kompensasiya məxaric və mədaxil eyni anda edilə bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)

            if (compensation_income is not None):
                initial_balance = calculate_holding_total_balance()
                office_initial_balance = calculate_office_balance(office=office)

                user = request.user
                customer = contract.customer

                note = f"GroupLeader - {contract_group_leader.fullname}, müştəri - {customer.fullname}, date - {now_date_date}, müqavilə düşən statusuna keçirildiyi üçün. Kompensasiya məbləği => {compensation_income}"
                c_income(cashbox, float(compensation_income),
                          contract_group_leader, note)

                contract.contract_status = CANCELLED
                contract.compensation_income = request.data.get("compensation_income")
                contract.save()
                
                subsequent_balance = calculate_holding_total_balance()
                office_subsequent_balance = calculate_office_balance(office=office)
                cashflow_create(
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
                    return Response({"detail": "Kompensasiya məxaric məbləği Ofisin balansından çox ola bilməz"},
                                    status=status.HTTP_400_BAD_REQUEST)
                initial_balance = calculate_holding_total_balance()
                office_initial_balance = calculate_office_balance(office=office)

                user = request.user
                customer = contract.customer

                note = f"GroupLeader - {contract_group_leader.fullname}, müştəri - {customer.fullname}, tarix - {now_date_date}, müqavilə düşən statusuna keçirildiyi üçün. Kompensasiya məbləği => {compensation_expense}"
                expense(cashbox, float(compensation_expense),
                          contract_group_leader, note)

                contract.contract_status = CANCELLED
                contract.compensation_expense = request.data.get("compensation_expense")
                contract.save()

                subsequent_balance = calculate_holding_total_balance()
                office_subsequent_balance = calculate_office_balance(office=office)
                cashflow_create(
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

            if (compensation_income == None and compensation_expense == None):
                contract.contract_status = CANCELLED
                contract.save()

            contract_group_leader = contract.group_leader
            contract_manager1 = contract.manager1

            try:
                warehouse = get_object_or_404(Warehouse, office=contract.office)
            except:
                return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

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

            # -------------------- Kommisiyaların geri alınması --------------------
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
                    if (group_leader_status is not None):
                        group_leader_prim = GroupLeaderPrimNew.objects.get(
                            prim_status=group_leader_status, position=group_leader.position)
                        group_leader_salary_view_current_month = SalaryView.objects.get(
                            employee=contract_group_leader, date=f"{now.year}-{now.month}-{1}")
                        group_leader_salary_view_next_month = SalaryView.objects.get(
                            employee=contract_group_leader, date=next_m)

                        group_leader_salary_view_current_month.sale_quantity = float(
                            group_leader_salary_view_current_month.sale_quantity) - float(product_quantity)
                        group_leader_salary_view_current_month.sales_amount = float(
                            group_leader_salary_view_current_month.sales_amount) - (float(contract.product.price) * float(contract.product_quantity))

                        if contract_payment_style == CASH:
                            group_leader_salary_view_next_month.final_salary = float(
                                group_leader_salary_view_next_month.final_salary) - (float(group_leader_prim.cash) * float(contract.product_quantity))
                        elif contract_payment_style == INSTALLMENT:
                            if int(contract_loan_term) >= 0 and int(contract_loan_term) <= 3:
                                group_leader_salary_view_next_month.final_salary = float(
                                    group_leader_salary_view_next_month.final_salary) - (float(group_leader_prim.cash) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 4 and int(contract_loan_term) <= 12:
                                group_leader_salary_view_next_month.final_salary = float(group_leader_salary_view_next_month.final_salary) - (
                                    float(group_leader_prim.installment_4_12) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 13 and int(contract_loan_term) <= 18:
                                group_leader_salary_view_next_month.final_salary = float(group_leader_salary_view_next_month.final_salary) - (
                                    float(group_leader_prim.installment_13_18) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 19 and int(contract_loan_term) <= 24:
                                group_leader_salary_view_next_month.final_salary = float(group_leader_salary_view_next_month.final_salary) - (
                                    float(group_leader_prim.installment_19_24) * float(contract.product_quantity))

                        group_leader_salary_view_current_month.save()
                        group_leader_salary_view_next_month.save()

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
                        manager1_salary_view_current_month = SalaryView.objects.get(
                            employee=contract_manager1, date=f"{now.year}-{now.month}-{1}")
                        manager1_salary_view_next_month = SalaryView.objects.get(
                            employee=contract_manager1, date=next_m)

                        manager1_salary_view_current_month.sale_quantity = float(
                            manager1_salary_view_current_month.sale_quantity) - float(product_quantity)
                        manager1_salary_view_current_month.sales_amount = float(manager1_salary_view_current_month.sales_amount) - (
                            float(contract.product.price) * float(contract.product_quantity))

                        if contract_payment_style == CASH:
                            manager1_salary_view_next_month.final_salary = float(
                                manager1_salary_view_next_month.final_salary) - (float(manager1_prim.cash) * float(contract.product_quantity))
                        elif contract_payment_style == INSTALLMENT:
                            if int(contract_loan_term) >= 0 and int(contract_loan_term) <= 3:
                                manager1_salary_view_next_month.final_salary = float(
                                    manager1_salary_view_next_month.final_salary) - (float(manager1_prim.cash) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 4 and int(contract_loan_term) <= 12:
                                manager1_salary_view_next_month.final_salary = float(manager1_salary_view_next_month.final_salary) - (
                                    float(manager1_prim.installment_4_12) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 13 and int(contract_loan_term) <= 18:
                                manager1_salary_view_next_month.final_salary = float(manager1_salary_view_next_month.final_salary) - (
                                    float(manager1_prim.installment_13_18) * float(contract.product_quantity))
                            elif int(contract_loan_term) >= 19 and int(contract_loan_term) <= 24:
                                manager1_salary_view_next_month.final_salary = float(manager1_salary_view_next_month.final_salary) - (
                                    float(manager1_prim.installment_19_24) * float(contract.product_quantity))

                        manager1_salary_view_current_month.save()
                        manager1_salary_view_next_month.save()

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
                        officeLeader_salary_view_next_month = SalaryView.objects.get(
                            employee=officeLeader, date=next_m)

                        officeLeader_salary_view_this_month.sale_quantity = float(
                            officeLeader_salary_view_this_month.sale_quantity) - float(product_quantity)
                        officeLeader_salary_view_this_month.sales_amount = float(officeLeader_salary_view_this_month.sales_amount) - (float(contract.product.price) * float(contract.product_quantity))
                        officeLeader_salary_view_this_month.save()

                        officeLeader_salary_view_next_month.final_salary = float(
                            officeLeader_salary_view_next_month.final_salary) - (float(officeleader_prim.prim_for_office) * float(contract.product_quantity))
                        officeLeader_salary_view_next_month.save()
            
            # -------------------- -------------------- --------------------
            contract.cancelled_date = datetime.date.today()
            contract.contract_status = CANCELLED
            contract.is_remove = True
            contract.note = contract_note
            contract.save()
            
            return Response({"detail": "Müqavilə düşən statusuna keçirildi"}, status=status.HTTP_200_OK)
        # Ilkin ödənişlərin ödənməsi
        if (contract.payment_style == INSTALLMENT):
            if (wants_to_pay_initial_payment != None and initial_payment_status == CONTINUING):
                if (float(wants_to_pay_initial_payment) != initial_payment):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
                elif (float(wants_to_pay_initial_payment) == initial_payment):
                    contract.initial_payment_status = "BİTMİŞ"
                    contract.initial_payment_date = now_date_date
                    contract.remaining_debt = float(contract.remaining_debt) - float(initial_payment)
                    contract.save()
                    return Response({"detail": "İlkin ödəniş ödənildi"}, status=status.HTTP_200_OK)

            if (wants_to_pay_debt_initial_payment != None and initial_payment_status == "BİTMİŞ" and initial_payment_debt_status == CONTINUING):
                if (float(wants_to_pay_debt_initial_payment) == initial_payment_debt):
                    contract.initial_payment_debt_status = "BİTMİŞ"
                    contract.initial_payment_debt_date = now_date_date
                    contract.remaining_debt = float(contract.remaining_debt) - float(initial_payment_debt)
                    contract.save()
                    return Response({"detail": "Qalıq ilkin ödəniş ödənildi"}, status=status.HTTP_200_OK)
                elif (float(wants_to_pay_debt_initial_payment) != initial_payment_debt):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "Bu əməliyyatı icra etmək mümkün olmadı"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception:
        traceback.print_exc()
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)
