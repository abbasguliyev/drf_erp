from services import INSTALLMENT, CASH
from services.models import Service, ServicePayment
from rest_framework.exceptions import ValidationError
from warehouse.api.selectors import warehouse_list, stock_list

def service_create(
        *, user = None,
        appointment_date = None,
        service_date = None,
        customer=None,
        contract=None,
        product,
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
    
    if is_auto == True:
        if contract is None:
            if customer is None:
                raise ValidationError({'detail': 'Müştəri daxil edilməyib'})
            if int(product_quantity) != len(product):
                raise ValidationError({'detail': 'Məhsullar listinin və saylar listinin uzunluqları bir-birinə bərabər deyil'})
        else:
            customer = contract.customer
            pr = contract.product_quantity
            product_quantity = [pr]

        if user is not None:
            operator = user
        
        total_price = 0
        for i, prod in enumerate(product):
            prod_price = prod.price
            total_price = total_price + (prod_price*int(product_quantity[i]))

        price = total_price
        total_paid_amount = initial_payment
        remaining_payment = float(price) - float(initial_payment) - float(discount)
        
        if discount is None:
            discount = 0

        if discount > remaining_payment:
            raise ValidationError({"detail":"Endirim qiyməti servis qiymətindən çox ola bilməz"})

        if initial_payment is None:
            initial_payment = 0

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