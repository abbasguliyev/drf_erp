import datetime
from rest_framework.exceptions import ValidationError
from services.models import ServicePayment
from services.api.selectors import service_payment_list
from warehouse.api.selectors import warehouse_list, stock_list
from warehouse.api.services.stock_service import reduce_product_from_stock
from cashbox.api.selectors import office_cashbox_list

def service_payment_create(
    *, service,
    service_amount: float = 0,
    is_done: bool = False,
    payment_date = None,
) -> ServicePayment:
    obj = ServicePayment.objects.create(
        service=service,
        service_amount=service_amount,
        is_done=is_done,
        payment_date=payment_date
    )
    obj.full_clean()
    obj.save()

    return obj

def service_payment_update(instance, **data) -> ServicePayment:
    if instance.service.is_auto == True:
        if instance.service.contract is not None:
            try:
                office = instance.service.contract.office
            except:
                office = None
        elif instance.service.service_creditor is not None:
            try:
                office = instance.service.service_creditor.office
            except:
                office = None
        elif instance.service.operator is not None:
            try:
                office = instance.service.operator.office
            except:
                office = None
        else:
            office = None
    else:
        if instance.service.service_creditor is not None:
            try:
                office = instance.service.service_creditor.office
            except:
                office = None
        elif instance.service.operator is not None:
            try:
                office = instance.service.operator.office
            except:
                office = None
        else:
            office = None

    if office is None:
        raise ValidationError({'detail': 'Əməliyyatı icra etmək üçün ofis tapılmadı, zəhmət olmasa daxil edilən məlumatların doğruluğunu yoxlayın'})
    
    is_done = data.get('is_done')
    if is_done is None:
        is_done = instance.is_done

    service_amount = data.get('service_amount')
    if service_amount is None:
        service_amount = instance.service_amount
    

    if is_done == True:
        products = instance.service.product.all()
        product_quantity = instance.service.product_quantity
        product_quantity_list = product_quantity.split(',')

        warehouse = warehouse_list().filter(office=office).last()
        for i, product in enumerate(products):
            print(f"{i=}")
            print(f"{product=}")
            stock = stock_list().filter(warehouse=warehouse, product=product).last()
            if stock is None:
                continue
            reduce_product_from_stock(stock=stock, product_quantity=int(product_quantity_list[i]))
            instance.is_done = True
            instance.payment_date = datetime.date.today()
            instance.save()
        
        cashbox = office_cashbox_list().filter(office=office).last()
        cashbox.balance = cashbox.balance + service_amount
        cashbox.save()

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