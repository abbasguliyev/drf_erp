from django.contrib.auth import get_user_model
from django.db.models import F, Q
from celery import shared_task
import pandas as pd
from contract.models import Contract
from contract.api.selectors import contract_list
from .models import Service, ServiceProductForContract
from services.api.services import service_model_services, service_payment_services
from services.api.selectors import service_list, service_product_for_contract_list
from . import CASH, INSTALLMENT

import datetime

User = get_user_model()

@shared_task(name='create_services_task')
def create_services_task(id):
    instance = contract_list().filter(id=id).last()
    contract_date = instance.contract_date

    contract_product_guarantee = instance.product.guarantee
    service_guarantee = contract_product_guarantee * 30.05

    service_products_for_contract = service_product_for_contract_list().filter(company=instance.company)
    date_format = '%d-%m-%Y'
    for service_product in service_products_for_contract:
        service_period = service_product.service_period
        product = [service_product.product]
        service_product_quantity = "1"

        d = pd.to_datetime(f"{contract_date.day}-{contract_date.month}-{contract_date.year}").strftime("%d-%m-%Y")
        month_service = pd.date_range(start=d, periods=2, freq=f'{service_period}M')[1]
        if contract_date.day < 29:
            date = datetime.datetime.strptime(f"{contract_date.day}-{month_service.month}-{month_service.year}", date_format)
        elif month_service.day > contract_date.day:
            date = datetime.datetime.strptime(f"{contract_date.day}-{month_service.month}-{month_service.year}", date_format)
        else:
            date = datetime.datetime.strptime(f"{month_service.day}-{month_service.month}-{month_service.year}", date_format)

        q = 0
        while(q < instance.product_quantity):
            price = 0
            for p in product:
                price += p.price
            
            if(contract_date.day < 29):
                service_model_services.service_create(
                    contract=instance,
                    customer=instance.customer,
                    product=product,
                    product_quantity=service_product_quantity,
                    pay_method=CASH,
                    price=price,
                    create_date=date,
                    is_auto=True,
                    guarantee=service_guarantee
                )
            elif(contract_date.day == 31 or contract_date.day == 30 or contract_date.day == 29):
                if(month_service.day <= contract_date.day):
                    service_model_services.service_create(
                        contract=instance,
                        customer=instance.customer,
                        product=product,
                        product_quantity=service_product_quantity,
                        pay_method=CASH,
                        price=price,
                        create_date=date,
                        is_auto=True,
                        guarantee=service_guarantee
                    )
                elif(month_service.day > contract_date.day):
                    service_model_services.service_create(
                        contract=instance,
                        customer=instance.customer,
                        product=product,
                        product_quantity=service_product_quantity,
                        pay_method=CASH,
                        price=price,
                        create_date=date,
                        is_auto=True,
                        guarantee=service_guarantee
                    )
            q += 1

@shared_task(name='create_service_payment_task')
def create_service_payment_task(id):
    instance = service_list().filter(pk=id).last()
    loan_term = instance.loan_term
    pay_method = instance.pay_method

    if int(loan_term) == 0:
        loan_term = 1
    
    discount = instance.discount
    if discount == None:
        discount = 0

    initial_payment = instance.initial_payment
    if initial_payment == None:
        initial_payment = 0

    price = instance.remaining_payment
    result1 = price // loan_term
    result2 = result1 * (loan_term - 1)
    last_month = price - result2
    
    service_date_str = instance.start_date_of_payment

    try:
        service_date = datetime.datetime.strptime(f"{service_date_str.day}-{service_date_str.month}-{service_date_str.year}", '%d-%m-%Y')
    except:
        service_date = service_date_str

    inc_month = pd.date_range(service_date, periods=loan_term+1, freq='M')

    if pay_method == CASH:
        service_payment_services.service_payment_create(
            service=instance, 
            service_amount=last_month,
            payment_date=f"{service_date.year}-{service_date.month}-{service_date.day}"
        )
    elif pay_method == INSTALLMENT:
        service_payment_services.installment_service_payment_create(
            loan_term=loan_term, service_date=service_date, inc_month=inc_month,
            last_month=last_month, service=instance, result1=result1
        )

@shared_task(name='task_that_reduce_guarantee_of_service_every_day')
def task_that_reduce_guarantee_of_service_every_day():
    """
    servisin qarantiyasını hər gün 1 vahid azaldan task
    """
    services = service_list().filter(Q(guarantee__gt=0) & ~Q(guarantee=None)).update(guarantee=F('guarantee') - 1)