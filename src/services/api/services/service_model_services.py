import datetime
from rest_framework.exceptions import ValidationError
from services import INSTALLMENT, CASH
from services.models import Service
from services.api.selectors import service_list, service_payment_list
from services.api.services import service_payment_services
from cashbox.api.decorators import cashbox_operation_decorator
import pandas as pd

from warehouse.api.selectors import warehouse_list, stock_list, holding_warehouse_list
from warehouse.api.services import warehouse_service, warehouse_history_service
from warehouse.api.services.stock_service import reduce_product_from_stock
from warehouse import SERVIS

def service_create(
    *, user = None,
    appointment_date = None,
    service_date = None,
    create_date = None,
    customer=None,
    contract=None,
    product=None,
    product_quantity = None,
    pay_method: str = CASH,
    price: float = 0,
    total_paid_amount: float = 0,
    remaining_payment: float = 0,
    loan_term: int = None,
    discount: float = 0,
    initial_payment: float = 0,
    note: str = None,
    service_creditor = None,
    operator=None,
    is_auto: bool = False,
    delay:bool = False,
    delay_date = None,
    start_date_of_payment = None,
    guarantee: int = None,
    is_finished: bool = False
) -> Service:
    if pay_method == INSTALLMENT:
        if loan_term is None:
            raise ValidationError({'detail': 'Ödəmə üsulu kredit seçilərsə, kredit müddəti daxil edilməlidir'})
        elif (loan_term == 0) or (loan_term == 1):
            raise ValidationError({"detail": "Ödəmə üsulu kredit seçilərsə, kredit müddəti 0 və ya 1 daxil edilə bilməz"})
        elif loan_term > 4:
            raise ValidationError({'detail': 'Kredit müddəti maksimum 4 ay seçilə bilər.'})
        else:
            loan_term = loan_term
    elif pay_method == CASH:
        if loan_term is not None:
            raise ValidationError({'detail': 'Ödəmə üsulu nəğd seçilərsə, kredit müddəti daxil edilməməlidir'})
        loan_term = 0
    
    if is_auto == True:
        if contract is None:
            if customer is None:
                raise ValidationError({'detail': 'Müştəri daxil edilməyib'})
        else:
            customer = contract.customer
        
    if create_date is None:
        create_date = datetime.date.today()

    if user is not None:
        operator = user
    
    if discount is None:
        discount = 0

    if initial_payment is None:
        initial_payment = 0

    if start_date_of_payment is None:
        if appointment_date is not None:
            start_date_of_payment = appointment_date
        else:
            start_date_of_payment = create_date

    if product is not None:
        if product_quantity is not None:
            product_quantity_list = product_quantity.split(',')
        else:
            product_quantity_list = ['1']
            product = []

        if len(product_quantity_list) != len(product):
            raise ValidationError({'detail': 'Məhsullar listinin və saylar listinin uzunluqları bir-birinə bərabər deyil'})

        total_price = 0
        for i, prod in enumerate(product):
            prod_price = prod.price
            total_price = total_price + (prod_price*int(product_quantity_list[i]))
        price = total_price
    
        if initial_payment > price:
            raise ValidationError({"detail":"İlkin ödəniş qiyməti servis qiymətindən çox ola bilməz"})
        
        if discount > (float(price) - float(initial_payment)):
            raise ValidationError({"detail":"Endirim qiyməti servis qiymətindən çox ola bilməz"})
        
        # remaining_payment = float(price) - float(initial_payment) - float(discount)
        remaining_payment = float(price) - float(discount)

    obj = Service.objects.create(
        appointment_date = appointment_date,
        create_date = create_date,
        service_date = service_date,
        customer=customer,
        contract=contract,
        product_quantity=product_quantity,
        pay_method=pay_method,
        price=price,
        total_paid_amount=0,
        remaining_payment=remaining_payment,
        loan_term=loan_term,
        discount=discount,
        initial_payment=initial_payment,
        note=note,
        service_creditor=service_creditor,
        operator=operator,
        is_auto=is_auto,
        delay=delay,
        delay_date=delay_date,
        start_date_of_payment=start_date_of_payment,
        guarantee = guarantee,
        is_finished = is_finished
    )
    obj.product.set(product)
    obj.full_clean()
    obj.save()

    return obj

def service_update(user, instance, **data):
    if instance.is_done == True:
        raise ValidationError({'detail': 'Servis artıq yerinə yetirilib.'})

    start_date_of_payment = data.get("start_date_of_payment")
    if start_date_of_payment is None:
        start_date_of_payment = instance.start_date_of_payment

    service_date_str = start_date_of_payment

    try:
        service_date = datetime.datetime.strptime(
            f"{service_date_str.day}-{service_date_str.month}-{service_date_str.year}", '%d-%m-%Y')
    except:
        service_date = service_date_str

    service_payments = service_payment_list().filter(service=instance)

    is_done = data.get('is_done')
    if is_done is None:
        is_done = instance.is_done

    loan_term = data.get('loan_term')
    if loan_term is None:
        loan_term = instance.loan_term

    pay_method = data.get('pay_method')
    discount = data.get('discount')
    initial_payment = data.get('initial_payment')
    note = data.get('note')

    inc_month = pd.date_range(service_date, periods=loan_term+1, freq='M')

    product = data.get('product')
    product_quantity = data.get('product_quantity')

    if product is not None and product_quantity is None:
        raise ValidationError({'detail': 'Yeni məhsul əlavə olunarkən, sayda əlavə edilməlidir'})
    elif product_quantity is not None and product is None:
        raise ValidationError({'detail': 'Yeni say əlavə olunub, amma məhsul əlavə olunmayıb'})
    
    if product_quantity is not None:
        product_quantity_list = product_quantity.split(',')

    if product is not None:
        if len(product_quantity_list) != len(product):
            raise ValidationError({'detail': 'Məhsullar listinin və saylar listinin uzunluqları bir-birinə bərabər deyil'})

        previous_product_list = instance.product.all()

        previous_product_quantity_str = instance.product_quantity
        previous_product_quantity_list = previous_product_quantity_str.split(',')
        new_products = [new_product for new_product in product if new_product not in previous_product_list]
        new_product_quantity = [new_product_quantity for new_product_quantity in product_quantity_list if new_product_quantity not in previous_product_quantity_list]
        if len(new_product_quantity) == 0:
            new_product_quantity = product_quantity_list
        total_price = 0
        for i, prod in enumerate(new_products):
            prod_price = prod.price
            total_price = total_price + (prod_price*int(new_product_quantity[i]))
        price = instance.price + total_price
        
        remaining_payment = float(price) - float(instance.total_paid_amount) - float(instance.discount)
        
        instance.price = price
        instance.remaining_payment = remaining_payment

        if instance.pay_method == CASH:
            service_payment = service_payments.last()
            if service_payment.is_done == False:
                service_payment_services.service_payment_update(
                    instance=service_payment, 
                    service_amount=remaining_payment, 
                    payment_date=f"{service_date.year}-{service_date.month}-{service_date.day}"
                )
        else:
            service_payments = service_payment_list().filter(service=instance)
            for service_payment in service_payments:
                service_payment.delete()

            price = instance.remaining_payment
            result1 = price // loan_term
            result2 = result1 * (loan_term - 1)
            last_month = price - result2
            service_payment_services.installment_service_payment_create(
                loan_term=loan_term, service_date=service_date, inc_month=inc_month,
                last_month=last_month, service=instance, result1=result1
            )

        instance.save()

    if instance.pay_method == CASH and pay_method == INSTALLMENT:
        price = instance.remaining_payment
        
        if initial_payment is None:
            initial_payment = 0

        if discount is None:
            discount = 0
        

        if discount > (float(price) - float(initial_payment)):
            raise ValidationError({"detail":"Endirim qiyməti servis qiymətindən çox ola bilməz"})

        if initial_payment > (float(price) - float(discount)):
            raise ValidationError({"detail":"İlkin ödəniş qiyməti servis qiymətindən çox ola bilməz"})
        
        service_payments = service_payment_list().filter(service=instance)
        for service_payment in service_payments:
            service_payment.delete()

        price = float(price) - float(discount) - float(initial_payment)

        if loan_term is None:
            loan_term = 1
        
        result1 = price // loan_term
        result2 = result1 * (loan_term - 1)
        last_month = price - result2
        service_payment_services.installment_service_payment_create(
            loan_term=loan_term, service_date=service_date, inc_month=inc_month,
            last_month=last_month, service=instance, result1=result1
        )

        instance.initial_payment = initial_payment
        instance.discount = discount
        instance.remaining_payment = price
        instance.pay_method = INSTALLMENT
        instance.save()

    if is_done == True:
        do_service_is_done(employee = user, service=instance, note=note)
    
    obj = service_list().filter(pk=instance.id).update(**data)
    return obj

def do_service_is_done(employee, service, note=None):
    """
    Servisi icra edildi statusuna keciren funksiya
    """

    products = service.product.all()
    product_quantity = service.product_quantity
    product_quantity_list = product_quantity.split(',')

    for i, product in enumerate(products):
        """
        Bu for döngüsünün yazilmasinda meqsed odur ki, eger stokda mehsullardan her hansi biri yoxdursa xeta 
        verecek ve proses bas vermeyecek
        """
        holding_warehouse = holding_warehouse_list().filter(product=product).last()
        if holding_warehouse is None:
            raise ValidationError({'detail': 'Xəta baş verdi. Servis məhsullarının stokda olub olmadığın dəqiqləşdirin.'})
        else:
            if holding_warehouse.useful_product_count < int(product_quantity_list[i]):
                raise ValidationError({'detail': 'Xəta baş verdi. Servis məhsullarının stokda yetəri qədər olub olmadığın dəqiqləşdirin.'})

    for i, product in enumerate(products):
        holding_warehouse = holding_warehouse_list().filter(product=product).last()
        sender_previous_quantity = holding_warehouse.quantity
        holding_warehouse.quantity = holding_warehouse.quantity - int(product_quantity)
        holding_warehouse.useful_product_count = holding_warehouse.useful_product_count - int(product_quantity)
        holding_warehouse.save()
        sender_subsequent_quantity = holding_warehouse.quantity

        warehouse_history_service.warehouse_history_create(
            user = employee, sender_warehouse="Holding anbarı", 
            sender_previous_quantity=sender_previous_quantity, sender_subsequent_quantity=sender_subsequent_quantity,
            product=product.product_name, quantity = product_quantity, operation_style=SERVIS, executor=employee,
            customer=service.customer, note=note
        )

    service.is_done = True
    service.service_date = datetime.date.today()
    service.save()

    if service.initial_payment > 0:
        pay_service_initial_payment(employee=employee, service=service, amount=service.initial_payment, func_name="pay_service_initial_payment")

    if service.pay_method == CASH:
        service_payment_instance = service_payment_list().filter(service=service).last()
        service_payment_services.service_payment_update(
            instance=service_payment_instance, user=employee, is_done=True
        )

@cashbox_operation_decorator
def pay_service_initial_payment(employee, service, amount, func_name="pay_service_initial_payment"):
    service.remaining_payment = float(service.remaining_payment) - float(amount)
    service.total_paid_amount = amount
    service.save()