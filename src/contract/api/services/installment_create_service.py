import datetime
import pandas as pd
from rest_framework.exceptions import ValidationError
from contract import INSTALLMENT
from contract.models import  Installment
from contract.api.selectors import contract_list, installment_list
from product.api.selectors import product_list

def create_installment_for_loan_term(
    *, loan_term, 
    inc_month, 
    payment_amount_for_last_month, 
    payment_amount_for_month,
    contract,
    month_num,
    now
):
    current_last_installment = installment_list().filter(contract=contract, last_month=True).last()
    if current_last_installment is not None:
        current_last_installment.last_month = False
        current_last_installment.save()

    i = 1
    while i <= loan_term:
        if i == loan_term:
            if payment_amount_for_last_month > (payment_amount_for_month//2):
                if now.day < 29:
                    Installment.objects.create(
                        month_no=month_num,
                        contract=contract,
                        date=f"{inc_month[i].year}-{inc_month[i].month}-{now.day}",
                        price=payment_amount_for_last_month,
                        last_month=True
                    ).save()
                elif now.day == 31 or now.day == 30 or now.day == 29:
                    if inc_month[i].day <= now.day:
                        Installment.objects.create(
                            month_no=month_num,
                            contract=contract,
                            date=f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                            price=payment_amount_for_last_month,
                            last_month=True
                        ).save()
                    elif inc_month[i].day > now.day:
                        Installment.objects.create(
                            month_no=month_num,
                            contract=contract,
                            date=f"{inc_month[i].year}-{inc_month[i].month}-{now.day}",
                            price=payment_amount_for_last_month,
                            last_month=True
                        ).save()
            else:
                last_installment = installment_list().filter(contract=contract, month_no=month_num-1).last()
                last_installment.price = last_installment.price + payment_amount_for_last_month
                last_installment.last_month = True
                last_installment.save()
        else:
            if now.day < 29:
                Installment.objects.create(
                    month_no=month_num,
                    contract=contract,
                    date=f"{inc_month[i].year}-{inc_month[i].month}-{now.day}",
                    price=payment_amount_for_month
                ).save()
            elif now.day == 31 or now.day == 30 or now.day == 29:
                if inc_month[i].day <= now.day:
                    Installment.objects.create(
                        month_no=month_num,
                        contract=contract,
                        date=f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                        price=payment_amount_for_month
                    ).save()
                if inc_month[i].day > now.day:
                    Installment.objects.create(
                        month_no=month_num,
                        contract=contract,
                        date=f"{inc_month[i].year}-{inc_month[i].month}-{now.day}",
                        price=payment_amount_for_month
                    ).save()
        month_num += 1
        i += 1

def installment_create(contract):
    loan_term = contract.loan_term

    if contract.payment_style == INSTALLMENT:
        now = contract.installment_start_date
        inc_month = pd.date_range(now, periods=loan_term+1, freq='M')
        initial_payment = contract.initial_payment
        initial_payment_debt = contract.initial_payment_debt

        if initial_payment is None:
            initial_payment = 0

        if initial_payment_debt is None:
            initial_payment_debt = 0

        total_amount = contract.total_amount
        initial_payment_total = initial_payment + initial_payment_debt

        total_payment_amount_for_month = total_amount - initial_payment_total

        payment_amount_for_month = total_payment_amount_for_month // loan_term

        debt = payment_amount_for_month * (loan_term - 1)
        payment_amount_for_last_month = total_payment_amount_for_month - debt

        if loan_term > 0:    
            create_installment_for_loan_term(
                loan_term=loan_term,
                inc_month=inc_month,
                payment_amount_for_last_month=payment_amount_for_last_month,
                payment_amount_for_month=payment_amount_for_month,
                contract=contract,
                month_num=1,
                now=now
            )
        

def create_test_installment(
    *, loan_term: int = 1,
    product_quantity: int = 1,
    installment_start_date,
    initial_payment: float = 0,
    initial_payment_debt: float = 0,
    discount: float = 0,
    product_id
):
    if loan_term > 24:
        raise ValidationError({"detail": "Maksimum kredit müddəti 24 aydır"})
    
    if initial_payment is None:
        initial_payment = 0
    if initial_payment_debt is None:
        initial_payment_debt = 0
    if discount is None:
        discount = 0

    product = product_list().filter(pk=product_id).last()

    now = installment_start_date
    inc_month = pd.date_range(now, periods = loan_term+1, freq='M')
    initial_payment = initial_payment
    initial_payment_debt = initial_payment_debt

    total_price = (product_quantity * product.price) - discount
    total_initial_payment = initial_payment + initial_payment_debt
    paid_total_amount_for_months = total_price - total_initial_payment

    if total_initial_payment >= total_price:
        raise ValidationError({'detail': 'İlkin ödəniş məbləği yekun məbləğdən kiçik olmalıdır.'})

    paid_amount_for_month = paid_total_amount_for_months // loan_term
    paid_amount_for_month = int(paid_amount_for_month)
    rest = paid_amount_for_month * (loan_term - 1)
    paid_amount_for_last_month = paid_total_amount_for_months - rest
    paid_amount_for_last_month = int(paid_amount_for_last_month)


    total_installment = []
    i = 1
    while i<=loan_term:
        if i == loan_term:
            if now.day < 29:
                installment = {}
                installment["month_no"] = i
                installment["date"] = datetime.datetime.strptime(f"{now.day}-{inc_month[i].month}-{inc_month[i].year}", '%d-%m-%Y').strftime('%d-%m-%Y')
                installment["price"] = paid_amount_for_last_month
                total_installment.append(installment)
            elif now.day == 31 or now.day == 30 or now.day == 29:
                if inc_month[i].day <= now.day:
                    installment = {}
                    installment["month_no"] = i
                    installment["date"] = datetime.datetime.strptime(f"{inc_month[i].day}-{inc_month[i].month}-{inc_month[i].year}", '%d-%m-%Y').strftime('%d-%m-%Y')
                    installment["price"] = paid_amount_for_last_month
                    total_installment.append(installment)
                    
                elif inc_month[i].day > now.day:
                    installment = {}
                    installment["month_no"] = i
                    installment["date"] = datetime.datetime.strptime(f"{now.day}-{inc_month[i].month}-{inc_month[i].year}", '%d-%m-%Y').strftime('%d-%m-%Y')
                    installment["price"] = paid_amount_for_last_month
                    total_installment.append(installment)
        else:
            if now.day < 29:
                installment = {}
                installment["month_no"] = i
                installment["date"] = datetime.datetime.strptime(f"{now.day}-{inc_month[i].month}-{inc_month[i].year}", '%d-%m-%Y').strftime('%d-%m-%Y')
                installment["price"] = paid_amount_for_month
                total_installment.append(installment)
                
            elif now.day == 31 or now.day == 30 or now.day == 29:
                if inc_month[i].day <= now.day:
                    installment = {}
                    installment["month_no"] = i
                    installment["date"] = datetime.datetime.strptime(f"{inc_month[i].day}-{inc_month[i].month}-{inc_month[i].year}", '%d-%m-%Y').strftime('%d-%m-%Y')
                    installment["price"] = paid_amount_for_month
                    total_installment.append(installment)
                    
                if inc_month[i].day > now.day:
                    installment = {}
                    installment["month_no"] = i
                    installment["date"] = datetime.datetime.strptime(f"{now.day}-{inc_month[i].month}-{inc_month[i].year}", '%d-%m-%Y').strftime('%d-%m-%Y')
                    installment["price"] = paid_amount_for_month
                    total_installment.append(installment)
        i+=1

    return total_installment