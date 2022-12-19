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

    service_products_for_contract = ServiceProductForContract.objects.prefetch_related("product").all()
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
                price += p.price
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