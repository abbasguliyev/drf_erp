from celery import shared_task
import pandas as pd
from contract.models import Contract
from django.contrib.auth import get_user_model
from .models import Service, ServiceProductForContract
import datetime

User = get_user_model()


@shared_task(name='create_services_task')
def create_services_task(id):
    instance = Contract.objects.get(id=id)
    now = instance.contract_date

    service_products_for_contract = ServiceProductForContract.objects.prefetch_related(
        "product").all()
    date_format = '%d-%m-%Y'
    for service_product in service_products_for_contract:
        service_period = service_product.service_period
        products = service_product.product.all()
        print(f"{products=}")
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
                price += float(p.price)
            if(now.day < 29):
                service = Service.objects.create(
                    contract=instance,
                    service_date=date_lt_29,
                    price=price,
                    is_auto=True
                )
            elif(now.day == 31 or now.day == 30 or now.day == 29):
                if(month_service.day <= now.day):
                    service = Service.objects.create(
                        contract=instance,
                        service_date=date_eq_29_29_30_31,
                        price=price,
                        is_auto=True
                    )
                elif(month_service.day > now.day):
                    service = Service.objects.create(
                        contract=instance,
                        service_date=date_lt_29,
                        price=price,
                        is_auto=True
                    )
            service.product.set(products)
            service.save()
            q += 1
# @shared_task(name='create_services_task')
# def create_services_task(id):
#     instance = Contract.objects.get(id=id)
#     now = instance.contract_date

#     d = pd.to_datetime(f"{now.day}-{now.month}-{now.year}")
#     month6 = pd.date_range(start=d, periods=2, freq='6M')[1]
#     month12 = pd.date_range(start=d, periods=2, freq='12M')[1]
#     month18 = pd.date_range(start=d, periods=2, freq='18M')[1]
#     month24 = pd.date_range(start=d, periods=2, freq='24M')[1]

#     kartric6ay = Product.objects.filter(kartric_novu="KARTRIC6AY", company=instance.company)
#     kartric12ay = Product.objects.filter(kartric_novu="KARTRIC12AY", company=instance.company)
#     kartric18ay = Product.objects.filter(kartric_novu="KARTRIC18AY", company=instance.company)
#     kartric24ay = Product.objects.filter(kartric_novu="KARTRIC24AY", company=instance.company)

#     date_format = '%d-%m-%Y'
#     kartric6ay_date_lt_29 = datetime.datetime.strptime(f"{now.day}-{month6.month}-{month6.year}", date_format)
#     kartric6ay_date_eq_29_30_31 = datetime.datetime.strptime(f"{month6.day}-{month6.month}-{month6.year}", date_format)

#     kartric12ay_date_lt_29 = datetime.datetime.strptime(f"{now.day}-{month12.month}-{month12.year}", date_format)
#     kartric12ay_date_eq_29_30_31 = datetime.datetime.strptime(f"{month12.day}-{month12.month}-{month12.year}", date_format)

#     kartric18ay_date_lt_29 = datetime.datetime.strptime(f"{now.day}-{month18.month}-{month18.year}", date_format)
#     kartric18ay_date_eq_29_30_31 = datetime.datetime.strptime(f"{month18.day}-{month18.month}-{month18.year}", date_format)

#     kartric24ay_date_lt_29 = datetime.datetime.strptime(f"{now.day}-{month24.month}-{month24.year}", date_format)
#     kartric24ay_date_eq_29_30_31 = datetime.datetime.strptime(f"{month24.day}-{month24.month}-{month24.year}", date_format)

#     q = 0
#     while(q<instance.product_quantity):
#         for i in range(1):
#             price = 0
#             for j in kartric6ay:
#                 price += float(j.price)
#             if(now.day < 29):
#                 service = Service.objects.create(
#                     contract=instance,
#                     service_date = kartric6ay_date_lt_29,
#                     price=price,
#                     is_auto=True
#                 )
#             elif(now.day == 31 or now.day == 30 or now.day == 29):
#                 if(month6.day <= now.day):
#                     service = Service.objects.create(
#                         contract=instance,
#                         service_date = kartric6ay_date_eq_29_30_31,
#                         price=price,
#                         is_auto=True
#                     )
#                 elif(month6.day > now.day):
#                     service = Service.objects.create(
#                         contract=instance,
#                         service_date = kartric6ay_date_lt_29,
#                         price=price,
#                         is_auto=True
#                     )
#             service.product.set(kartric6ay)
#             service.save()
#         for i in range(1):
#             price = 0
#             for j in kartric12ay:
#                 price += float(j.price)
#             if(now.day < 29):
#                 service = Service.objects.create(
#                     contract=instance,
#                     service_date = kartric12ay_date_lt_29,
#                     price=price,
#                     is_auto=True
#                 )
#             elif(now.day == 31 or now.day == 30 or now.day == 29):
#                 if(month12.day <= now.day):
#                     service = Service.objects.create(
#                         contract=instance,
#                         service_date = kartric12ay_date_eq_29_30_31,
#                         price=price,
#                         is_auto=True
#                     )
#                 elif(month12.day > now.day):
#                     service = Service.objects.create(
#                         contract=instance,
#                         service_date = kartric12ay_date_lt_29,
#                         price=price,
#                         is_auto=True
#                     )
#             service.product.set(kartric12ay)
#             service.save()
#         for i in range(1):
#             price = 0
#             for j in kartric18ay:
#                 price += float(j.price)
#             if(now.day < 29):
#                 service = Service.objects.create(
#                     contract=instance,
#                     service_date = kartric18ay_date_lt_29,
#                     price=price,
#                     is_auto=True
#                 )
#             elif(now.day == 31 or now.day == 30 or now.day == 29):
#                 if(month18.day <= now.day):
#                     service = Service.objects.create(
#                         contract=instance,
#                         service_date = kartric18ay_date_eq_29_30_31,
#                         price=price,
#                         is_auto=True
#                     )
#                 elif(month18.day > now.day):
#                     service = Service.objects.create(
#                         contract=instance,
#                         service_date = kartric18ay_date_lt_29,
#                         price=price,
#                         is_auto=True
#                     )
#             service.product.set(kartric18ay)
#             service.save()
#         for i in range(1):
#             price = 0
#             for j in kartric24ay:
#                 price += float(j.price)
#             if(now.day < 29):
#                 service = Service.objects.create(
#                     contract=instance,
#                     service_date = kartric24ay_date_lt_29,
#                     price=price,
#                     is_auto=True
#                 )
#             elif(now.day == 31 or now.day == 30 or now.day == 29):
#                 if(month24.day <= now.day):
#                     service = Service.objects.create(
#                         contract=instance,
#                         service_date = kartric24ay_date_eq_29_30_31,
#                         price=price,
#                         is_auto=True
#                     )
#                 elif(month24.day > now.day):
#                     service = Service.objects.create(
#                         contract=instance,
#                         service_date = kartric24ay_date_lt_29,
#                         price=price,
#                         is_auto=True
#                     )
#             service.product.set(kartric24ay)
#             service.save()
#         q+=1
