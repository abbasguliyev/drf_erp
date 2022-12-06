from datetime import date
from services import INSTALLMENT, CASH
from services.models import Service
from rest_framework.exceptions import ValidationError
from warehouse.api.selectors import warehouse_list
from warehouse.models import Warehouse, Stock


def service_create(
        *, pay_method: str,
        loan_term: int = None,
        discount: float = None,
        contract=None,
        product,
        customer=None,
        service_date: date = date.today(),
        price: float = 0,
        initial_payment: float = 0,
        note: str = None,
        is_auto: bool = False
) -> Service:
    if pay_method == INSTALLMENT:
        if loan_term is None:
            raise ValidationError({'detail': 'Ödəmə üsulu kredit seçilərsə, kredit müddəti daxil edilməlidir'})
        if (loan_term == 0) or (loan_term == 1):
            raise ValidationError(
                {"detail": "Ödəmə üsulu kredit seçilərsə, kredit müddəti 0 və ya 1 daxil edilə bilməz"})
    if discount is None:
        discount = 0
    if initial_payment is None:
        initial_payment = 0

    office = contract.office
    warehouse = warehouse_list().filter(office=office).last()
    # Aşağıda for-un 2 dəfə yazılmasında məqsəd, əgər stokda məhsullardan hər hansısa biri yoxdursa əvvəlcədən bilinsin
    # və stokdan heçbir məhsul çıxarılmasın
    # for product in products:
    #     try:
    #         stock = Stock.objects.get(warehouse=warehouse, product=product)
    #     except Exception:
    #         raise ValidationError({"detail": f"Anbarın stokunda {product.product_name} məhsulu yoxdur"})
    #
    # price = 0
    # for prod in products:
    #     price += prod.price
    #     try:
    #         stock = Stock.objects.get(warehouse=warehouse, product=prod)
    #         stock.decrease_stock(quantity=1)
    #         if stock.quantity == 0:
    #             stock.delete()
    #     except Exception:
    #         raise ValidationError({"detail": "Anbarın stokunda məhsul yoxdur"})

    obj = Service.objects.create(
        pay_method=pay_method,
        loan_term=loan_term,
        discount=discount,
        contract=contract,
        customer=customer,
        service_date=service_date,
        price=price,
        initial_payment=initial_payment,
        note=note,
        is_auto=is_auto
    )
    obj.product.set(product)
    obj.full_clean()
    obj.save()
