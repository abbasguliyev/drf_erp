import datetime
from cashbox.models import HoldingCashbox, OfficeCashbox, CashFlow, CompanyCashbox
from cashbox.api.selectors import (
    holding_cashbox_list,
    company_cashbox_list,
    office_cashbox_list
)
from company.api.selectors import holding_list

def calculate_holding_total_balance():
    total_balance = 0

    h_cashbox = holding_cashbox_list()
    holding_balance = 0
    for hk in h_cashbox:
        holding_balance += hk.balance

    c_cashbox = company_cashbox_list()
    company_balance = 0
    for sk in c_cashbox:
        company_balance += sk.balance

    o_cashbox = office_cashbox_list()
    office_balance = 0
    for ok in o_cashbox:
        office_balance += ok.balance

    total_balance = holding_balance + company_balance + office_balance
    return total_balance

def calculate_holding_balance():
    cashbox = holding_cashbox_list()[0]
    return cashbox.balance

def calculate_company_balance(company):
    cashbox = company_cashbox_list().filter(company= company).last()
    return cashbox.balance

def calculate_office_balance(office):
    cashbox = office_cashbox_list().filter(office=office).last()
    return cashbox.balance

def cashflow_create(
    holding=None, 
    company=None, 
    office=None, 
    date=datetime.date.today(), 
    operation_style=None, 
    description=None, 
    quantity=0, 
    executor=None,
    customer=None,
    personal=None,
    cost_type=None,
    balance=0
):
    """
    Pul axinlarini create eden funksiya
    """

    holding = holding_list().last()

    cashflow = CashFlow.objects.create(
        holding=holding,
        company=company,
        office=office,
        date=date,
        operation_style=operation_style,
        description=description,
        executor=executor,
        personal=personal,
        customer=customer,
        quantity=quantity,
        cost_type=cost_type,
        balance=balance
    )
    return cashflow.save()