import datetime
from cashbox.models import HoldingCashbox, OfficeCashbox, CashFlow, CompanyCashbox
from cashbox.api.selectors import (
    holding_cashbox_list,
    company_cashbox_list,
    office_cashbox_list,
    cash_flow_list,
    holding_cashbox_opr_list,
    company_cashbox_opr_list
)

def calculate_holding_total_balance():
    total_balance = 0

    h_cashbox = holding_cashbox_list()
    holding_balance = 0
    for hk in h_cashbox:
        holding_balance += float(hk.balance)

    c_cashbox = company_cashbox_list()
    company_balance = 0
    for sk in c_cashbox:
        company_balance += float(sk.balance)

    o_cashbox = office_cashbox_list()
    office_balance = 0
    for ok in o_cashbox:
        office_balance += float(ok.balance)

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
    balance=0
):
    """
    Pul axinlarini create eden funksiya
    """

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
        balance=balance
    )
    return cashflow.save()