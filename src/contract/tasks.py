import datetime
import time

from celery import shared_task
import pandas as pd
from django.contrib.auth import get_user_model
from .models import DemoSales, Contract
from account.api.selectors import user_list
from contract.api.services.installment_create_service import installment_create
from contract.api.selectors import contract_list, demo_sales_list, installment_list
from contract.api.services import installment_update_service
from services.api.selectors import service_list, service_payment_list

User = get_user_model()

@shared_task(name='demo_create_task')
def demo_create_task():
    users = user_list()

    now = datetime.date.today()

    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    for user in users:
        demos = demo_sales_list().filter(
            user=user,
            created_date__year=next_m.year,
            created_date__month=next_m.month
        )
        if len(demos) != 0:
            continue
        else:
            demo = DemoSales.objects.create(
                user=user, count=0, created_date=f"{next_m.year}-{next_m.month}-{1}").save()

    for user in users:
        demos = demo_sales_list().filter(
            user=user,
            created_date__year=now.year,
            created_date__month=now.month
        )
        if len(demos) != 0:
            continue
        else:
            demo = DemoSales.objects.create(
                user=user, count=0, created_date=f"{now.year}-{now.month}-{1}").save()

@shared_task(name='create_installment_task')
def create_installment_task(id):
    instance = contract_list().filter(id=id).last()
    installment_create(contract=instance)

@shared_task(name='pay_installment_task')
def pay_installment_task(user_id, installments):
    user = user_list().filter(pk=user_id).last()
    for installment_id in installments:
        installment = installment_list().filter(pk=installment_id).last()
        if installment.is_paid == False:
            installment_update_service.pay_installment(user=user, installment=installment, func_name="pay_installment")


@shared_task(name='demo_sale_count_task')
def demo_sale_count_task(id):
    instance = contract_list().filter(id=id).last()
    manager1 = instance.manager1
    manager2 = instance.manager2
    contract_date = instance.contract_date
    product_quantity = instance.product_quantity
    sale_count = 0
    try:
        manager1_demo = demo_sales_list().filter(user=manager1, created_date=contract_date)
        sale_count = sale_count + int(product_quantity)
        manager1_demo.sale_count = sale_count
        manager1_demo.save()
    except:
        sale_count = 0
    
    try:
        manager2_demo = demo_sales_list().filter(user=manager2, created_date=contract_date)
        sale_count = sale_count + int(product_quantity)
        manager2_demo.sale_count = sale_count
        manager2_demo.save()
    except:
        sale_count = 0


@shared_task(name='removed_contract_installments_delete_task')
def removed_contract_installments_delete_task(contract_id):
    old_contract = contract_list().filter(pk=contract_id).last()
    old_installmets = installment_list().filter(contract = old_contract, is_paid=False)
    for installment in old_installmets:
        installment.delete()

@shared_task(name='removed_contract_service_delete_task')
def removed_contract_service_delete_task(contract_id):
    contract = contract_list().filter(pk=contract_id).last()
    all_service = service_list().filter(contract=contract)
    for service in all_service:
        all_service_payment = service_payment_list().filter(service=service, is_done=False)
        if all_service_payment.count() > 0:
            for service_payment in all_service_payment:
                service_payment.delete()
        service.delete()
