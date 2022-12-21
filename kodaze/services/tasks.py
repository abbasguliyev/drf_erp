from celery import shared_task
import pandas as pd
from contract.models import Contract
from django.contrib.auth import get_user_model
from .models import Service, ServiceProductForContract
from services.api.services import service_model_services
from services.api.selectors import service_list
from . import CASH, INSTALLMENT

import datetime

User = get_user_model()

@shared_task(name='create_services_task')
def create_services_task(id):
    instance = Contract.objects.get(id=id)
    now = instance.contract_date

    service_products_for_contract = ServiceProductForContract.objects.prefetch_related("product").all()
    date_format = '%d-%m-%Y'
    for service_product in service_products_for_contract:
        service_period = service_product.service_period
        products = service_product.product.all()
        print(f"{products=}")
        service_product_quantity = list()
        for p in range(len(products)):
            service_product_quantity.append(1)

        d = pd.to_datetime(f"{now.day}-{now.month}-{now.year}")
        month_service = pd.date_range(
            start=d, periods=2, freq=f'{service_period}M')[1]

        date_lt_29 = datetime.datetime.strptime(
            f"{now.day}-{month_service.month}-{month_service.year}", date_format)
        date_eq_29_29_30_31 = datetime.datetime.strptime(
            f"{month_service.day}-{month_service.month}-{month_service.year}", date_format)

        q = 0
        while(q < instance.product_quantity):
            price = 0
            for p in products:
                price += p.price
            if(now.day < 29):
                service_model_services.service_create(
                    contract=instance,
                    customer=instance.customer,
                    product=products,
                    product_quantity=service_product_quantity,
                    pay_method=CASH,
                    price=price,
                    service_date=date_lt_29,
                    is_auto=True
                )
            elif(now.day == 31 or now.day == 30 or now.day == 29):
                if(month_service.day <= now.day):
                    service_model_services.service_create(
                        contract=instance,
                        customer=instance.customer,
                        product=products,
                        product_quantity=service_product_quantity,
                        pay_method=CASH,
                        price=price,
                        service_date=date_eq_29_29_30_31,
                        is_auto=True
                    )
                elif(month_service.day > now.day):
                    service_model_services.service_create(
                        contract=instance,
                        customer=instance.customer,
                        product=products,
                        product_quantity=service_product_quantity,
                        pay_method=CASH,
                        price=price,
                        service_date=date_lt_29,
                        is_auto=True
                    )
            q += 1

@shared_task(name='create_service_payment_task')
def create_service_payment_task(id):
    instance = service_list().filter(pk=id).last()
    loan_term = instance.loan_term
    pay_method = instance.pay_method

    if int(loan_term) == 0:
        loan_term = 1
    print(f"****************************{loan_term=}")
    print(f"****************************{pay_method=}")
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

    service_date_str = instance.create_date
    print(f"{service_date_str=}")

    try:
        service_date = datetime.datetime.strptime(
            f"{service_date_str.day}-{service_date_str.month}-{service_date_str.year}", '%d-%m-%Y')
    except:
        service_date = service_date_str

    inc_month = pd.date_range(service_date, periods=loan_term+1, freq='M')

    if pay_method == CASH:
        service_model_services.service_payment_create(
            service=instance, 
            service_amount=last_month,
            payment_date=f"{service_date.year}-{service_date.month}-{service_date.day}"
        )
    elif pay_method == INSTALLMENT:
        j = 1
        while(j <= int(loan_term)):
            if(j == int(loan_term)):
                if(service_date.day < 29):
                    service_model_services.service_payment_create(
                        service=instance, 
                        service_amount=last_month,
                        payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_date.day}"
                    )
                elif(service_date.day == 31 or service_date.day == 30 or service_date.day == 29):
                    if(inc_month[j].day <= service_date.day):
                        service_model_services.service_payment_create(
                            service=instance, 
                            service_amount=last_month,
                            payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}"
                        )
                    elif(inc_month[j].day > service_date.day):
                        service_model_services.service_payment_create(
                            service=instance, 
                            service_amount=last_month,
                            payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_date.day}"
                        )
            else:
                if(service_date.day < 29):
                    service_model_services.service_payment_create(
                        service=instance, 
                        service_amount=result1,
                        payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_date.day}"
                    )
                elif(service_date.day == 31 or service_date.day == 30 or service_date.day == 29):
                    if(inc_month[j].day <= service_date.day):
                        service_model_services.service_payment_create(
                            service=instance, 
                            service_amount=result1,
                            payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}"
                        )
                    elif(inc_month[j].day > service_date.day):
                        service_model_services.service_payment_create(
                            service=instance, 
                            service_amount=result1,
                            payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_date.day}"
                        )
            j += 1