import datetime
from rest_framework.exceptions import ValidationError
from services.models import ServicePayment
from services.api.selectors import service_payment_list, service_product_for_contract_list
from services.api.services import service_model_services
from services import CASH

from warehouse.api.selectors import warehouse_list, stock_list
from warehouse.api.services.stock_service import reduce_product_from_stock
from cashbox import INCOME
from cashbox.api.selectors import office_cashbox_list
from product.api.selectors import product_list
from cashbox.api.services.cashbox_operation_services import holding_cashbox_operation_create
from salary.api.services.commission_services import creditor_permission_add_to_salary_view
import pandas as pd

def create_is_auto_services_when_update_service(contract, s_product, service_creditor=None):
    """
        Contract imzalanarken create olan servicelerin vaxti catdiqda ve
        yerine yetirildikde avtomatik yeni servislərin qurulmasina xidmet eden method
    """
    current_date = datetime.date.today()
    date_format = '%d-%m-%Y'
    create = False

    service_products_for_contract = service_product_for_contract_list().filter(company=contract.company)
    for service_product_for_contract in service_products_for_contract:
        service_product = service_product_for_contract.product
        if service_product == s_product:
            service_period = service_product_for_contract.service_period
            product = [service_product]
            service_product_quantity = "1"
            create = True

    if create == True:
        d = pd.to_datetime(f"{current_date.day}-{current_date.month}-{current_date.year}")
        month_service = pd.date_range(start=d, periods=2, freq=f'{service_period}M')[1]

        date_lt_29 = datetime.datetime.strptime(f"{current_date.day}-{month_service.month}-{month_service.year}", date_format)
        date_eq_29_29_30_31 = datetime.datetime.strptime(f"{month_service.day}-{month_service.month}-{month_service.year}", date_format)

        q = 0
        while q < contract.product_quantity:
            price = 0
            for p in product:
                price += p.price
            
            if current_date.day < 29:
                service_model_services.service_create(
                    contract=contract,
                    customer=contract.customer,
                    product=product,
                    product_quantity=service_product_quantity,
                    pay_method=CASH,
                    price=price,
                    create_date=date_lt_29,
                    is_auto=True,
                    service_creditor=service_creditor
                )
            elif current_date.day == 31 or current_date.day == 30 or current_date.day == 29:
                if month_service.day <= current_date.day:
                    service_model_services.service_create(
                        contract=contract,
                        customer=contract.customer,
                        product=product,
                        product_quantity=service_product_quantity,
                        pay_method=CASH,
                        price=price,
                        create_date=date_eq_29_29_30_31,
                        is_auto=True,
                        service_creditor=service_creditor
                    )
                elif month_service.day > current_date.day:
                    service_model_services.service_create(
                        contract=contract,
                        customer=contract.customer,
                        product=product,
                        product_quantity=service_product_quantity,
                        pay_method=CASH,
                        price=price,
                        create_date=date_lt_29,
                        is_auto=True,
                        service_creditor=service_creditor
                    )
            q += 1


def service_payment_create(
    *, service,
    service_amount: float = 0,
    is_done: bool = False,
    payment_date = None,
    service_paid_date = None,
    note = None
) -> ServicePayment:
    obj = ServicePayment.objects.create(
        service=service,
        service_amount=service_amount,
        is_done=is_done,
        payment_date=payment_date,
        service_paid_date=service_paid_date,
        note = note
    )
    obj.full_clean()
    obj.save()

    return obj

def service_payment_update(instance, user=None, **data) -> ServicePayment:
    is_done = data.get('is_done')

    service_amount = data.get('service_amount')
    if service_amount is None:
        service_amount = instance.service_amount

    if instance.is_done == True and is_done == True:
        raise ValidationError({"detail": "Servis artıq ödənilib"})
    elif instance.is_done == True and is_done == False:
        raise ValidationError({"detail": "Ödənilmiş servisi təkrar ödənilməmiş etmək mümkün deyil"})

    if instance.is_done == False and is_done == True:
        products = instance.service.product.all()
        
        service_payments = service_payment_list().filter(service=instance.service).order_by("pk")
        if instance == service_payments.last():
            if instance.service.is_auto == True:
                products = instance.service.product.all()
                s_product = products.last()
                create_is_auto_services_when_update_service(contract=instance.service.contract, s_product=s_product, service_creditor=instance.service.service_creditor)

            if instance.service.is_done == False:
                instance.service.is_done = True
                instance.service.service_date = datetime.date.today()
            instance.service.total_paid_amount += service_amount
            instance.service.remaining_payment -= service_amount
            instance.service.is_finished = True
            instance.service.save()
        else:
            instance.service.total_paid_amount += service_amount
            instance.service.remaining_payment -= service_amount
            instance.service.save()
        
        instance.is_done = True
        instance.service_paid_date = datetime.datetime.now()
        instance.service_paid_amount = service_amount
        instance.remaining_debt = instance.service.remaining_payment
        instance.save()

        creditor = instance.service.service_creditor

        note = f"{instance.service.customer.fullname} müştərisinin servis ödənişi"
        holding_cashbox_operation_create(executor=user, personal=creditor, amount=service_amount, note=note, operation=INCOME)
        
        if creditor is not None:
            creditor_permission_add_to_salary_view(employee=creditor, amount=service_amount, date=datetime.date.today(), func_name="creditor_permission")
    
    obj = service_payment_list().filter(pk=instance.id).update(**data)
    return obj

def installment_service_payment_create(
    *, loan_term: int = 1, 
    service_date,
    inc_month,
    last_month,
    service,
    result1
):
    j = 1
    while(j <= int(loan_term)):
        if(j == int(loan_term)):
            if(service_date.day < 29):
                service_payment_create(
                    service=service, 
                    service_amount=last_month,
                    payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_date.day}"
                )
            elif(service_date.day == 31 or service_date.day == 30 or service_date.day == 29):
                if(inc_month[j].day <= service_date.day):
                    service_payment_create(
                        service=service, 
                        service_amount=last_month,
                        payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}"
                    )
                elif(inc_month[j].day > service_date.day):
                    service_payment_create(
                        service=service, 
                        service_amount=last_month,
                        payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_date.day}"
                    )
        else:
            if(service_date.day < 29):
                service_payment_create(
                    service=service, 
                    service_amount=result1,
                    payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_date.day}"
                )
            elif(service_date.day == 31 or service_date.day == 30 or service_date.day == 29):
                if(inc_month[j].day <= service_date.day):
                    service_payment_create(
                        service=service, 
                        service_amount=result1,
                        payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}"
                    )
                elif(inc_month[j].day > service_date.day):
                    service_payment_create(
                        service=service, 
                        service_amount=result1,
                        payment_date=f"{inc_month[j].year}-{inc_month[j].month}-{service_date.day}"
                    )
        j += 1


def test_installment_service_create(
    *, product, 
    product_quantity,
    start_date_of_payment,
    loan_term,
    initial_payment,
    discount
) -> list:
    product_quantity_list = product_quantity.split(',')
    total_price = 0
    if loan_term > 4:
        raise ValidationError({'detail': 'Kredit müddəti maksimum 4 ay ola bilər'})

    for i, prod in enumerate(product):
        product_model = product_list().filter(pk=prod).last()
        if product_model is None:
            raise ValidationError({'detail': 'Məhsul tapılmadı'})
        prod_price = product_model.price
        total_price = total_price + (prod_price*int(product_quantity_list[i]))
    price = total_price
    remaining_payment = float(price) - float(initial_payment) - float(discount)
    if remaining_payment <= 0:
        raise ValidationError({'detail': 'Məlumatları doğru daxil edin'})
    
    
    price = remaining_payment
    result1 = price // loan_term
    result1 = int(result1)
    result2 = result1 * (loan_term - 1)
    last_month = price - result2
    last_month = int(last_month)

    service_date_str = start_date_of_payment
    service_date = datetime.datetime.strptime(service_date_str, '%d-%m-%Y')

    inc_month = pd.date_range(service_date, periods=loan_term+1, freq='M')

    test_service_payments = []

    j = 1
    while(j <= int(loan_term)):
        if(j == int(loan_term)):
            if(service_date.day < 29):
                service_payment = {}
                service_payment['service_amount'] = last_month
                service_payment['payment_date'] = datetime.datetime.strptime(f"{service_date.day}-{inc_month[j].month}-{inc_month[j].year}", '%d-%m-%Y').strftime('%d-%m-%Y')
                test_service_payments.append(service_payment)
            elif(service_date.day == 31 or service_date.day == 30 or service_date.day == 29):
                if(inc_month[j].day <= service_date.day):
                    service_payment = {}
                    service_payment['service_amount'] = last_month
                    service_payment['payment_date'] = datetime.datetime.strptime(f"{inc_month[j].day}-{inc_month[j].month}-{inc_month[j].year}", '%d-%m-%Y').strftime('%d-%m-%Y')
                    test_service_payments.append(service_payment)
                elif(inc_month[j].day > service_date.day):
                    service_payment = {}
                    service_payment['service_amount'] = last_month
                    service_payment['payment_date'] = datetime.datetime.strptime(f"{service_date.day}-{inc_month[j].month}-{inc_month[j].year}", '%d-%m-%Y').strftime('%d-%m-%Y')
                    test_service_payments.append(service_payment)
        else:
            if(service_date.day < 29):
                service_payment = {}
                service_payment['service_amount'] = result1
                service_payment['payment_date'] = datetime.datetime.strptime(f"{service_date.day}-{inc_month[j].month}-{inc_month[j].year}", '%d-%m-%Y').strftime('%d-%m-%Y')
                test_service_payments.append(service_payment)
            elif(service_date.day == 31 or service_date.day == 30 or service_date.day == 29):
                if(inc_month[j].day <= service_date.day):
                    service_payment = {}
                    service_payment['service_amount'] = result1
                    service_payment['payment_date'] = datetime.datetime.strptime(f"{inc_month[j].day}-{inc_month[j].month}-{inc_month[j].year}", '%d-%m-%Y').strftime('%d-%m-%Y')
                    test_service_payments.append(service_payment)
                elif(inc_month[j].day > service_date.day):
                    service_payment = {}
                    service_payment['service_amount'] = result1
                    service_payment['payment_date'] = datetime.datetime.strptime(f"{service_date.day}-{inc_month[j].month}-{inc_month[j].year}", '%d-%m-%Y').strftime('%d-%m-%Y')
                    test_service_payments.append(service_payment)
        j += 1
    
    return test_service_payments