import math
from rest_framework import status
from rest_framework.response import Response
from account.models import User, Customer
from api.v1.contract.serializers import ContractSerializer
from company.models import Office, Section, Position
from cashbox.models import OfficeCashbox
from income_expense.models import OfficeCashboxIncome, OfficeCashboxExpense
from salary.models import (
    Manager1PrimNew, 
    SalaryView, 
    OfficeLeaderPrim, 
    GroupLeaderPrimNew
)
from contract.models import Installment
from warehouse.models import (
    Warehouse,
    Stock
)
from product.models import Product
from services.models import Service, ServicePayment
from rest_framework.generics import get_object_or_404
import pandas as pd
import datetime
import traceback
from services.signals import create_services

from api.v1.utils.ocean_contract_pdf_create import (
    ocean_contract_pdf_canvas,
    ocean_create_contract_pdf,
    ocean_installment_contract_pdf_canvas,
    ocean_installment_create_contract_pdf,
)

from api.v1.utils.magnus_contract_pdf_create import (
    magnus_create_contract_pdf,
    magnus_contract_pdf_canvas,
    magnus_installment_create_contract_pdf,
    magnus_installment_contract_pdf_canvas,
)

from api.v1.cashbox.utils import (
    calculate_holding_total_balance, 
    cashflow_create, 
    calculate_office_balance, 
)

import django

def create_and_add_pdf_when_contract_updated(sender, instance, created, **kwargs):
    if created:
        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.office.company.name == okean:
            contract_pdf_canvas_list = ocean_contract_pdf_canvas(
                contract=instance, customer=instance.customer
            )
            contract_pdf = ocean_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        elif instance.office.company.name == magnus:
            contract_pdf_canvas_list = magnus_contract_pdf_canvas(
                contract=instance, customer=instance.customer
            )
            contract_pdf = magnus_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        instance.pdf = contract_pdf
        instance.save()

def create_and_add_pdf_when_contract_installment_updated(sender, instance, created, **kwargs):
    if created:
        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.office.company.name == okean:
            contract_pdf_canvas_list = ocean_installment_contract_pdf_canvas(
                contract=instance
            )
            contract_pdf = ocean_installment_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        elif instance.office.company.name == magnus:
            contract_pdf_canvas_list = magnus_installment_contract_pdf_canvas(
                contract=instance
            )
            contract_pdf = magnus_installment_create_contract_pdf(
                contract_pdf_canvas_list, instance)
        instance.pdf_elave = contract_pdf
        instance.save()

def pdf_create_when_contract_updated(sender, instance, created):
    create_and_add_pdf_when_contract_updated(
        sender=sender, instance=instance, created=created)
    create_and_add_pdf_when_contract_installment_updated(
        sender=sender, instance=instance, created=created)
# ----------------------------------------------------------------------------------------------------------------------

def reduce_product_from_stock(stock, product_quantity):
    # stock.quantity = stock.quantity - int(product_quantity)
    stock.decrease_stock(int(product_quantity))
    stock.save()
    if (stock.quantity == 0):
        stock.delete()
    return stock.quantity


def add_product_to_stock(stock, product_quantity):
    # stock.quantity = stock.quantity + int(product_quantity)
    stock.increase_stock(int(product_quantity))
    stock.save()
    return stock.quantity


def c_income(company_cashbox, the_amount_to_enter, responsible_employee_1, note):
    total_balance = float(the_amount_to_enter) + float(company_cashbox.balance)
    company_cashbox.balance = total_balance
    company_cashbox.save()
    date = datetime.date.today()

    income = OfficeCashboxIncome.objects.create(
        executor=responsible_employee_1,
        cashbox=company_cashbox,
        amount=the_amount_to_enter,
        date=date,
        note=note
    )
    income.save()
    return income


def expense(company_cashbox, the_amount_to_enter, responsible_employee_1, note):
    total_balance = float(company_cashbox.balance) - float(the_amount_to_enter)
    company_cashbox.balance = total_balance
    company_cashbox.save()
    date = datetime.date.today()

    expense = OfficeCashboxExpense.objects.create(
        executor=responsible_employee_1,
        cashbox=company_cashbox,
        amount=the_amount_to_enter,
        date=date,
        note=note
    )
    expense.save()
    return expense