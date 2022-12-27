import datetime
from rest_framework.exceptions import ValidationError
from services import INSTALLMENT, CASH
from services.models import Service
from services.api.selectors import service_list, service_payment_list
from services.api.services import service_payment_services

def service_create(
    *, user = None,
    appointment_date = None,
    service_date = None,
    customer=None,
    contract=None,
    product=None,
    product_quantity,
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
) -> Service:
    if pay_method == INSTALLMENT:
        if loan_term is None:
            raise ValidationError({'detail': 'Ödəmə üsulu kredit seçilərsə, kredit müddəti daxil edilməlidir'})
        elif (loan_term == 0) or (loan_term == 1):
            raise ValidationError(
                {"detail": "Ödəmə üsulu kredit seçilərsə, kredit müddəti 0 və ya 1 daxil edilə bilməz"})
        else:
            loan_term = loan_term
    elif pay_method == CASH:
        if loan_term is not None:
            raise ValidationError({'detail': 'Ödəmə üsulu nəğd seçilərsə, kredit müddəti daxil edilməməlidir'})

        loan_term = 0
    
    product_quantity_list = product_quantity.split(',')

    if is_auto == True:
        if contract is None:
            if customer is None:
                raise ValidationError({'detail': 'Müştəri daxil edilməyib'})
        else:
            customer = contract.customer

    if user is not None:
        operator = user
    
    if discount is None:
        discount = 0

    if initial_payment is None:
        initial_payment = 0

    if product is not None:
        if len(product_quantity_list) != len(product):
            raise ValidationError({'detail': 'Məhsullar listinin və saylar listinin uzunluqları bir-birinə bərabər deyil'})

        total_price = 0
        for i, prod in enumerate(product):
            prod_price = prod.price
            total_price = total_price + (prod_price*int(product_quantity_list[i]))
        price = total_price
        total_paid_amount = initial_payment
        remaining_payment = float(price) - float(initial_payment) - float(discount)
    
        if discount > remaining_payment:
            raise ValidationError({"detail":"Endirim qiyməti servis qiymətindən çox ola bilməz"})

    obj = Service.objects.create(
        appointment_date = appointment_date,
        service_date = service_date,
        customer=customer,
        contract=contract,
        product_quantity=product_quantity,
        pay_method=pay_method,
        price=price,
        total_paid_amount=total_paid_amount,
        remaining_payment=remaining_payment,
        loan_term=loan_term,
        discount=discount,
        initial_payment=initial_payment,
        note=note,
        service_creditor=service_creditor,
        operator=operator,
        is_auto=is_auto,
        delay=delay,
        delay_date=delay_date
    )
    obj.product.set(product)
    obj.full_clean()
    obj.save()

    return obj

def service_update(instance, **data):
    if instance.is_auto == True:
        if instance.contract is not None:
            try:
                office = instance.contract.office
            except:
                office = None
        elif instance.service_creditor is not None:
            try:
                office = instance.service_creditor.office
            except:
                office = None
        elif instance.operator is not None:
            try:
                office = instance.operator.office
            except:
                office = None
        else:
            office = None
    else:
        if instance.service_creditor is not None:
            try:
                office = instance.service_creditor.office
            except:
                office = None
        elif instance.operator is not None:
            try:
                office = instance.operator.office
            except:
                office = None
        else:
            office = None

    if office is None:
        raise ValidationError({'detail': 'Əməliyyatı icra etmək üçün ofis tapılmadı, zəhmət olmasa daxil edilən məlumatların doğruluğunu yoxlayın'})

    service_payments = service_payment_list().filter(service=instance)

    is_done = data.get('is_done')
    if is_done is None:
        is_done = instance.is_done

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

        if instance.is_done == True:
            raise ValidationError({'detail': 'Servis artıq yerinə yetirilib.'})

        previous_product_list = instance.product.all()

        previous_product_quantity_str = instance.product_quantity
        previous_product_quantity_list = previous_product_quantity_str.split(',')
        
        new_products = [new_product for new_product in product if new_product not in previous_product_list]
        new_product_quantity = [new_product_quantity for new_product_quantity in product_quantity_list if new_product_quantity not in previous_product_quantity_list]

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
                service_payment_services.service_payment_update(instance=service_payment, salary_amount=remaining_payment)
        else:
            unpaid_service_payments = service_payment_list().filter(service=instance, is_done=False).delete()
            paid_service_payments = service_payment_list().filter(service=instance, is_done=True)

            for unpaid_service_payment in unpaid_service_payments:
                price = instance.remaining_payment
                result1 = price // (instance.loan_term - unpaid_service_payments.count())
                result2 = result1 * (instance.loan_term - 1)
                last_month = price - result2
                # service_payment_update(instance=unpaid_service_payment, salary_amount=)
        
        instance.save()

    if is_done == True:
        do_service_is_done(service=instance)
    
    obj = service_list().filter(pk=instance.id).update(**data)
    return obj

def do_service_is_done(service):
    """
    Servisi odenildi statusuna keciren funksiya
    """
    service_payments = service_payment_list().filter(service=service)
    service.is_done = True
    service.service_date = datetime.date.today()
    service.save()

    for service_payment in service_payments:
        service_payment_services.service_payment_update(instance=service_payment)