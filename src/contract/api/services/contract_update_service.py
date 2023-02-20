import datetime
import math
import pandas as pd
from django.db import transaction
from rest_framework.exceptions import ValidationError
from cashbox.api.decorators import cashbox_operation_decorator
from contract.api.services.installment_create_service import create_installment_for_loan_term
from contract import FINISHED, AZALTMAQ, ARTIRMAQ, CONTINUING, CANCELLED, REMOVED
from contract.tasks import removed_contract_installments_delete_task, removed_contract_service_delete_task
from contract.api.selectors import installment_list, contract_list
from salary.api.utils import return_commission_after_cancel_contract
from services.api.selectors import service_payment_list, service_list

from warehouse.api.services.stock_service import stock_create
from warehouse.api.services.warehouse_service import holding_warehouse_create
from warehouse.api.services import warehouse_history_service
from warehouse.api.selectors import warehouse_list, stock_list, holding_warehouse_list
from warehouse import SOKUNTU

@cashbox_operation_decorator
def pay_initial_payment_debt(user, contract, initial_payment_amount, func_name="pay_initial_payment_debt"):
    """
    Qalıq ilkin ödəniş ödəmə funksiyası
    """
    initial_payment_debt_status = contract.initial_payment_debt_status
    initial_payment_debt = contract.initial_payment_debt

    if initial_payment_debt_status == CONTINUING:
        if initial_payment_amount != initial_payment_debt:
            raise ValidationError({"detail": "Məbləği düzgün daxil edin"})
        
        if initial_payment_amount == initial_payment_debt:
            contract.initial_payment_debt_status = FINISHED
            contract.paid_initial_payment_debt = initial_payment_amount
            contract.initial_payment_debt_paid_date = datetime.datetime.now()
            contract.remaining_debt = contract.remaining_debt - initial_payment_debt
            contract.save()

def update_contract(instance, **data):
    obj = contract_list().filter().update(**data)
    return obj

@cashbox_operation_decorator
def compensation_income_func(user, contract, compensation_income, note=None, func_name = "compensation_income_func"):
    """
    Söküntü zamanı kompensasiya mədaxil funksiyası
    """
    contract.contract_status = CANCELLED
    contract.intervention_product_status = REMOVED
    contract.intervention_date = datetime.date.today()
    contract.contract_removed_date = datetime.date.today()
    contract.compensation_income = compensation_income
    contract.note = note
    contract.save()

@cashbox_operation_decorator
def compensation_expense_func(user, contract, compensation_expense, note=None, func_name = "compensation_expense_func"):
    """
    Söküntü zamanı kompensasiya məxaric funksiyası
    """
    contract.contract_status = CANCELLED
    contract.intervention_product_status = REMOVED
    contract.intervention_date = datetime.date.today()
    contract.contract_removed_date = datetime.date.today()
    contract.compensation_expense = compensation_expense
    contract.note = note
    contract.save()


def remove_contract(*, user, contract, compensation_income=None, compensation_expense=None, note=None):
    """
    Müqavilə düşən statusuna keçərkən bu hissə işə düşür
    """
    office = contract.office
    is_holding_contract = contract.is_holding_contract
    product = contract.product
    product_quantity = contract.product_quantity

    if contract.contract_status == CANCELLED:
        raise ValidationError({"detail": "Müqavilə artıq düşən statusundadır."})
    
    if contract.contract_status == FINISHED:
        raise ValidationError({"detail": "Müqavilə artıq bitib."})

    if (compensation_income is not None and compensation_expense is not None):
        raise ValidationError({"detail": "Kompensasiya məxaric və mədaxil eyni anda edilə bilməz"})

    if compensation_income == None and compensation_expense == None:
        contract.contract_status = CANCELLED
        contract.intervention_product_status = REMOVED
        contract.intervention_date = datetime.date.today()
        contract.contract_removed_date = datetime.date.today()
        contract.note = note
        contract.save()
    elif compensation_income is not None:
        compensation_income_func(
            user=user, 
            contract=contract, 
            compensation_income=compensation_income,
            func_name = "compensation_income_func",
            note=note
        )
    elif compensation_expense is not None:
        compensation_expense_func(
            user=user, 
            contract=contract, 
            compensation_expense=compensation_expense,
            func_name = "compensation_expense_func",
            note=note
        )

    warehouse = warehouse_list().filter(office=office).last()
    if is_holding_contract == False:
        stock = stock_list().filter(warehouse=warehouse, product=product).last()
        if stock is None:
            sender_previous_quantity = 0
            
            stock_create(warehouse=warehouse, product=product, quantity=product_quantity, changed_product_count=product_quantity)
            
            sender_subsequent_quantity = product_quantity
        else:
            sender_previous_quantity = stock.quantity

            stock.quantity = stock.quantity + product_quantity
            stock.changed_product_count = stock.changed_product_count + product_quantity
            stock.save()
            
            sender_subsequent_quantity = stock.quantity
        
        sender_warehouse = warehouse.name
    else:
        stock = holding_warehouse_list().filter(product=product).last()
        
        if stock is None:
            sender_previous_quantity = 0
            
            holding_warehouse_create(
                product=product, 
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
        product=product.product_name, quantity = product_quantity, operation_style=SOKUNTU, executor=user, note=note,
        customer=contract.customer
    )

    transaction.on_commit(lambda: removed_contract_service_delete_task.delay(contract.id))
    transaction.on_commit(lambda: removed_contract_installments_delete_task.delay(contract.id))

    # -------------------- Kommisiyaların geri alınması --------------------
    return_commission_after_cancel_contract(contract)
    # -------------------- -------------------- ----------------------------
