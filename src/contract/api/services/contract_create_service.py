import datetime
from rest_framework.exceptions import ValidationError

from account import HOLDING

from cashbox.api.decorators import cashbox_operation_decorator
from company.api.selectors import holding_list

from contract import FINISHED, CONTINUING
from contract.models import Contract
from contract import CASH, CONTINUING, INSTALLMENT

from warehouse.api.services.stock_service import reduce_product_from_stock
from warehouse.api.services import warehouse_history_service
from warehouse.api.selectors import warehouse_list, stock_list, holding_warehouse_list
from warehouse import SATIS, DEYISIM


def total_amount(product_price, product_quantity, discount=0):
    product_total_price = product_price * product_quantity
    if discount > product_total_price:
        raise ValidationError({'detail': 'Endirim məbləği ümumi məbləğdən çox ola bilməz'})
    total_amount = product_total_price - discount
    return total_amount

@cashbox_operation_decorator
def cash_contract_create(
    *, user=None, group_leader=None, manager1=None, manager2=None, customer, product, region, address,
    product_quantity: int = 1, electronic_signature=None, contract_date=None, company=None, office=None, 
    note=None, payment_style=None, holding=None, total_price, discount=0, func_name = "cash_contract",
    changed_new_contract=False, old_contract=None
) -> Contract:
    """
    Nəğd Müqavilə
    """
    if holding is not None:
        is_holding_contract = True
    else:
        is_holding_contract = False

    if office is not None:
        company = office.company

    obj = Contract.objects.create(
        group_leader = group_leader,
        manager1=manager1,
        manager2=manager2,
        customer=customer,
        product=product,
        product_quantity=product_quantity,
        electronic_signature=electronic_signature,
        contract_date=contract_date,
        company=company,
        office=office,
        note=note,
        payment_style=payment_style,
        remaining_debt=0,
        contract_status=FINISHED,
        total_amount=total_price,
        is_holding_contract = is_holding_contract,
        region=region,
        address=address,
        discount=discount,
        changed_new_contract=changed_new_contract,
        old_contract=old_contract
    )
    obj.full_clean()
    obj.save()
    return obj

@cashbox_operation_decorator
def installment_contract_create(
    *, user=None, group_leader=None, manager1=None, manager2=None, customer, product, product_quantity: int = 1,
    region, address, electronic_signature=None, contract_date=None, company=None, office=None, loan_term=None, 
    initial_payment=None, initial_payment_date=None, initial_payment_debt=None, initial_payment_debt_date=None,
    note=None, payment_style=None, total_price, holding, intervention_product_status=None,
    installment_start_date=None, remaining_debt=0, initial_payment_status=None, initial_payment_debt_status=None,
    func_name = "installment_contract", discount=0, changed_new_contract=False, old_contract=None
) -> Contract:
    """
    Kreditli Müqavilə
    """
    if loan_term is None:
        raise ValidationError({"detail": "Ödəmə statusu kreditdir amma kredit müddəti daxil edilməyib"})
    elif loan_term == 0:
        raise ValidationError({"detail": "Ödəmə statusu kreditdir amma kredit müddəti 0 daxil edilib"})
    elif loan_term > 24:
        raise ValidationError({"detail": "Maksimum kredit müddəti 24 aydır"})

    if initial_payment is not None:
        initial_payment_date = datetime.date.today()
        initial_payment_paid_date = datetime.datetime.now()
        
        initial_payment_status = FINISHED
        if initial_payment == 0 and initial_payment_debt is not None:
            raise ValidationError({"detail": "İlkin ödəniş daxil edilmədən qalıq ilkin ödəniş daxil edilə bilməz"})
        if initial_payment >= total_price:
            raise ValidationError({"detail": "İlkin ödəniş məbləği müqavilənin məbləğindən az olmalıdır"})
        if datetime.date.today() > initial_payment_date:
            raise ValidationError({"detail": "İlkin ödəniş tarixini keçmiş tarixə təyin edə bilməzsiniz"})
        if initial_payment_debt is not None:
            if initial_payment_debt_date is None:
                raise ValidationError({'detail': 'Qalıq İlkin ödəniş məbləği qeyd olunub amma qalıq ilkin ödəniş tarixi qeyd olunmayıb'})
            elif initial_payment_date == initial_payment_debt_date:
                raise ValidationError({"detail": "İlkin ödəniş qalıq və ilkin ödəniş hər ikisi eyni tarixə qeyd oluna bilməz"})
            elif initial_payment_date > initial_payment_debt_date:
                raise ValidationError({"detail": "İlkin ödəniş qalıq tarixi ilkin ödəniş tarixindən əvvəl ola bilməz"})
            if initial_payment_debt >= (total_price - initial_payment):
                raise ValidationError({"detail": "Ümumi ilkin ödəniş məbləği müqavilənin məbləğindən az olmalıdır"})
    else:
        initial_payment = 0
        initial_payment_date = None
        initial_payment_paid_date = None
        if initial_payment_debt is not None:
            raise ValidationError({"detail": "İlkin ödəniş daxil edilmədən qalıq ilkin ödəniş daxil edilə bilməz"})

    if initial_payment_debt is None:
        initial_payment_debt = 0
    else:
        initial_payment_debt_status = CONTINUING

    if installment_start_date is None:
        if contract_date is not None:
            installment_start_date = contract_date
        else:
            installment_start_date = datetime.date.today()
    else:
        installment_start_date = f"{contract_date.year}-{contract_date.month}-{installment_start_date.day}"
    
    if remaining_debt == 0:
        remaining_debt = total_price - (initial_payment + initial_payment_debt)
    else:
        remaining_debt = remaining_debt
        
    if holding is not None:
        is_holding_contract = True
    else:
        is_holding_contract = False

    total_amount = total_price
    initial_payment_total = initial_payment + initial_payment_debt

    total_payment_amount_for_month = total_amount - initial_payment_total
    payment_amount_for_month = total_payment_amount_for_month // loan_term

    default_installment_amount=payment_amount_for_month

    obj = Contract.objects.create(
        group_leader = group_leader,
        manager1=manager1,
        manager2=manager2,
        customer=customer,
        product=product,
        product_quantity=product_quantity,
        electronic_signature=electronic_signature,
        contract_date=contract_date,
        installment_start_date=installment_start_date,
        company=company,
        office=office,
        note=note,
        payment_style=payment_style,
        contract_status=CONTINUING,
        total_amount=total_price,
        remaining_debt=remaining_debt,
        is_holding_contract=is_holding_contract,
        initial_payment=initial_payment,
        paid_initial_payment=initial_payment,
        initial_payment_date=initial_payment_date,
        initial_payment_paid_date=initial_payment_paid_date,
        initial_payment_debt=initial_payment_debt,
        initial_payment_debt_date=initial_payment_debt_date,
        initial_payment_status=initial_payment_status,
        initial_payment_debt_status=initial_payment_debt_status,
        intervention_product_status=intervention_product_status,
        loan_term=loan_term,
        changed_new_contract=changed_new_contract,
        default_installment_amount=default_installment_amount,
        region=region,
        address=address,
        discount=discount,
        old_contract=old_contract
    )
    obj.full_clean()
    obj.save()
    return obj


def create_contract(
    *, user=None, group_leader=None, manager1=None, manager2=None, customer, region, address, product, product_quantity: int = 1,
    electronic_signature=None, contract_date=None, company=None, office=None, loan_term=None, 
    initial_payment=None, initial_payment_date=None, initial_payment_debt=None, initial_payment_debt_date=None,
    paid_initial_payment=None, paid_initial_payment_debt=None, initial_payment_paid_date=None, initial_payment_debt_paid_date=None,
    note=None, payment_style=None, installment_start_date=None, intervention_product_status=None, remaining_debt=0,
    initial_payment_status=None, initial_payment_debt_status=None, total_price=None, func_name=None, cancelled_contract=False,
    changed_new_contract=False, is_conditional_contract=None, discount=0, old_contract=None
) -> Contract:
    if group_leader is None:
        group_leader = user

    if contract_date is None:
        contract_date = datetime.date.today()

    if func_name is None:
        func_name = "installment_contract"
        
    holding = None
    if total_price is None:
        total_price = total_amount(product.price, product_quantity, discount)

    if group_leader.register_type != HOLDING:
        if office is None:
            office = group_leader.office
        
        try:
            company = office.company
        except:
            company = None
        
        try:
            warehouse = warehouse_list().filter(office=office).last()
            if warehouse is None:
                raise ValidationError({'detail': 'Anbar tapılmadı'})

            stock = stock_list().filter(warehouse=warehouse, product=product).last()
            sender_warehouse = warehouse.name
        except:
            holding = holding_list().last()
            stock = holding_warehouse_list().filter(product=product).last()
            sender_warehouse = "Holding anbarı"
    else:
        holding = holding_list().last()
        stock = holding_warehouse_list().filter(product=product).last()
        sender_warehouse = "Holding anbarı"
        company = None

    if stock is None:
        raise ValidationError({"detail": "Stokda yetəri qədər məhsul yoxdur"})

    if stock.useful_product_count < product_quantity:
        raise ValidationError({"detail": "Stokda yetəri qədər məhsul yoxdur"})

    sender_previous_quantity = stock.quantity

    if payment_style == CASH:
        contract = cash_contract_create(
            user = user, group_leader = group_leader, manager1=manager1, manager2=manager2, customer=customer, region=region,
            address=address, product=product, product_quantity=product_quantity, electronic_signature=electronic_signature, 
            contract_date=contract_date, company=company, office=office, note=note, payment_style=payment_style,
            holding=holding, total_price=total_price, discount=discount, func_name = "cash_contract", 
            changed_new_contract=changed_new_contract, old_contract=old_contract
        )
    elif payment_style == INSTALLMENT:
        contract = installment_contract_create(
            user = user, group_leader = group_leader, manager1=manager1, manager2=manager2, customer=customer, region=region,
            address=address, product=product, product_quantity=product_quantity, electronic_signature=electronic_signature, 
            contract_date=contract_date, installment_start_date=installment_start_date, company=company, office=office, 
            loan_term=loan_term, initial_payment=initial_payment, initial_payment_date=initial_payment_date, 
            initial_payment_debt=initial_payment_debt, initial_payment_debt_date=initial_payment_debt_date, 
            note=note, payment_style=payment_style, holding=holding, total_price=total_price,
            func_name = func_name, discount=discount, changed_new_contract=changed_new_contract, 
            old_contract=old_contract
        )

    reduce_product_from_stock(stock, product_quantity)
    sender_subsequent_quantity = stock.quantity

    if func_name == "change_contract":
        warehouse_history_service.warehouse_history_create(
            user = user, company=company, sender_warehouse=f"{sender_warehouse}",
            sender_previous_quantity=sender_previous_quantity, sender_subsequent_quantity=sender_subsequent_quantity,
            product=product.product_name, quantity = product_quantity, operation_style=DEYISIM, executor=user, note=note, 
            customer=customer
        )
    else:
        warehouse_history_service.warehouse_history_create(
            user = user, company=company, sender_warehouse=f"{sender_warehouse}",
            sender_previous_quantity=sender_previous_quantity, sender_subsequent_quantity=sender_subsequent_quantity,
            product=product.product_name, quantity = product_quantity, operation_style=SATIS, executor=user, note=note,
            customer=customer
        )

    return contract