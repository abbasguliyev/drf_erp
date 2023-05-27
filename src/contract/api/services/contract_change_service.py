import datetime
from django.db import transaction
from rest_framework.exceptions import ValidationError
from contract.api.selectors import installment_list
from contract.api.services import contract_create_service
from contract import CONTINUING, CASH
from contract.tasks import removed_contract_installments_delete_task, removed_contract_service_delete_task
from warehouse.api.services.stock_service import stock_create
from warehouse.api.services.warehouse_service import holding_warehouse_create
from warehouse.api.services import warehouse_history_service
from warehouse.api.selectors import warehouse_list, stock_list, holding_warehouse_list
from warehouse import DEYISIM
from services.api.selectors import service_list, service_payment_list


def change_contract_product_service(
    *, user=None,
    old_contract,
    product,  
    initial_payments: float,
    loan_term: int,
    discount: float = 0,
    note: str = None
):
    cash_contract = False

    if loan_term == None or loan_term == 1 or loan_term == 0:
        cash_contract = True

    if product == None:
        raise ValidationError({"detail": "Dəyişim statusunda məhsul əlavə olunmalıdır."})

    initial_payment = old_contract.initial_payment
    if initial_payment == None:
        initial_payment = 0
    initial_payment_debt = old_contract.initial_payment_debt
    initial_payment_debt_status = old_contract.initial_payment_debt_status
    if initial_payment_debt == None:
        initial_payment_debt = 0
    else:
        if initial_payment_debt_status == CONTINUING:
            initial_payment_debt = 0

    paid_amount = 0
    paid_installments = installment_list().filter(contract = old_contract, is_paid = True)
    if paid_installments.count() > 0:
        for paid_installment in paid_installments:
            paid_amount = paid_amount + paid_installment.price
    paid_amount = paid_amount + initial_payment + initial_payment_debt
    total_amount = (product.price * old_contract.product_quantity)

    if discount >= total_amount:
        raise ValidationError({'detail': 'Endirim qiyməti yeni məhsulun qiymətindən az olmalıdır'})

    total_amount = total_amount - discount
    remaining_debt = total_amount - paid_amount

    if total_amount <= paid_amount:
        cash_contract = True

    group_leader = old_contract.group_leader
    manager1 = old_contract.manager1
    manager2 = old_contract.manager2
    customer = old_contract.customer
    product_quantity = old_contract.product_quantity
    electronic_signature = old_contract.electronic_signature
    contract_date = datetime.date.today()
    company = old_contract.company
    office = old_contract.office
    initial_payment_date = datetime.date.today()
    payment_style = old_contract.payment_style
    installment_start_date = datetime.date.today()
    remaining_debt=remaining_debt
    region = old_contract.region
    address = old_contract.address
    is_holding_contract = old_contract.is_holding_contract
    changed_product = old_contract.product

    if cash_contract == False:
        contract_create_service.create_contract(
            user=user, group_leader=group_leader, manager1=manager1, manager2=manager2, customer=customer, 
            region=region, address=address, product=product, product_quantity=product_quantity, electronic_signature=electronic_signature, 
            contract_date=contract_date, installment_start_date=installment_start_date, company=company, 
            office=office, loan_term=loan_term, initial_payment=paid_amount, paid_initial_payment=initial_payments,
            initial_payment_date=initial_payment_date, initial_payment_paid_date=initial_payment_date, note=note, payment_style=payment_style, 
            total_price=total_amount, func_name="change_contract", discount=discount, 
            changed_new_contract=True, old_contract=old_contract
        )
    else:
        contract_create_service.create_contract(
            user=user, group_leader=group_leader, manager1=manager1, manager2=manager2, customer=customer, 
            region=region, address=address, product=product, product_quantity=product_quantity, electronic_signature=electronic_signature, 
            contract_date=contract_date, company=company, 
            office=office, loan_term=0, note=note, payment_style=CASH, 
            total_price=total_amount, func_name="change_contract", discount=discount, 
            changed_new_contract=True, old_contract=old_contract
        )

    old_contract.intervention_product_status = "DƏYİŞİLMİŞ MƏHSUL"
    old_contract.intervention_date = datetime.date.today()
    old_contract.contract_change_date = datetime.date.today()
    old_contract.contract_status = "DÜŞƏN"
    old_contract.cancelled_contract = True
    old_contract.save()
    
    # -------------------- Servislərin silinməsi --------------------
    transaction.on_commit(lambda: removed_contract_service_delete_task.delay(old_contract.id))
    # -------------------- Kreditlərin silinməsi --------------------
    transaction.on_commit(lambda: removed_contract_installments_delete_task.delay(old_contract.id))

    warehouse = warehouse_list().filter(office=office).last()
    if is_holding_contract == False:
        stock = stock_list().filter(warehouse=warehouse, product=changed_product).last()
        if stock is None:
            sender_previous_quantity = 0
            
            stock_create(warehouse=warehouse, product=changed_product, quantity=product_quantity, changed_product_count=product_quantity)
            
            sender_subsequent_quantity = product_quantity
        else:
            sender_previous_quantity = stock.quantity

            stock.quantity = stock.quantity + product_quantity
            stock.changed_product_count = stock.changed_product_count + product_quantity
            stock.save()
            
            sender_subsequent_quantity = stock.quantity
        
        sender_warehouse = warehouse.name
    else:
        stock = holding_warehouse_list().filter(product=changed_product).last()
        
        if stock is None:
            sender_previous_quantity = 0
            
            holding_warehouse_create(
                product=changed_product, 
                quantity=product_quantity,
                useful_product_count=0,
                unuseful_product_count=product_quantity
            )
            
            sender_subsequent_quantity = product_quantity
        else:
            sender_previous_quantity = stock.quantity
            
            stock.quantity = stock.quantity + product_quantity
            stock.unuseful_product_count = stock.unuseful_product_count + product_quantity
            stock.save()
            
            sender_subsequent_quantity = stock.quantity
        sender_warehouse = "Holding anbarı"

    warehouse_history_service.warehouse_history_create(
        user = user, sender_warehouse=f"{sender_warehouse}",
        sender_previous_quantity=sender_previous_quantity, sender_subsequent_quantity=sender_subsequent_quantity,
        product=changed_product.product_name, quantity = product_quantity, operation_style=DEYISIM, executor=user, note=note,
        customer=old_contract.customer
    )


def find_contract_paid_amount(contract) -> float:
    initial_payment = contract.initial_payment
    if initial_payment == None:
        initial_payment = 0
    initial_payment_debt = contract.initial_payment_debt
    initial_payment_debt_status = contract.initial_payment_debt_status
    if initial_payment_debt == None:
        initial_payment_debt = 0
    else:
        if initial_payment_debt_status == CONTINUING:
            initial_payment_debt = 0

    paid_amount = 0
    paid_installments = installment_list().filter(contract = contract, is_paid = True)

    if paid_installments.count() > 0:
        for paid_installment in paid_installments:
            paid_amount = paid_amount + paid_installment.price
    
    paid_amount = paid_amount + initial_payment + initial_payment_debt
    return paid_amount
