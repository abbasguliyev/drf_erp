import datetime
from cashbox.models import HoldingCashbox, OfficeCashbox, CashFlow, CompanyCashbox

def calculate_holding_total_balance():
    total_balance = 0

    cashbox = HoldingCashbox.objects.all()
    holding_balance = 0
    for hk in cashbox:
        holding_balance += float(hk.balance)

    cashbox = CompanyCashbox.objects.all()
    company_balance = 0
    for sk in cashbox:
        company_balance += float(sk.balance)

    cashbox = OfficeCashbox.objects.all()
    office_balance = 0
    for ok in cashbox:
        office_balance += float(ok.balance)

    total_balance = holding_balance + company_balance + office_balance
    return total_balance

def calculate_holding_balance():
    cashbox = HoldingCashbox.objects.all()[0]
    return cashbox.balance

def calculate_company_balance(company):
    cashbox = CompanyCashbox.objects.get(company=company)
    return cashbox.balance

def calculate_office_balance(office):
    cashbox = OfficeCashbox.objects.get(office=office)
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