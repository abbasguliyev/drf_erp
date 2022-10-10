import datetime
from cashbox.models import HoldingCashbox, OfficeCashbox, CashFlow, CompanyCashbox

def calculate_holding_total_balance():
    umumi_balance = 0

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

    umumi_balance = holding_balance + company_balance + office_balance
    return umumi_balance

def calculate_holding_balance():
    holding_balance = 0
    cashbox = HoldingCashbox.objects.all()[0]
    holding_balance += float(cashbox.balance)
    return holding_balance

def calculate_company_balance(company):
    company_balance = 0
    cashbox = CompanyCashbox.objects.get(company=company)
    company_balance += float(cashbox.balance)
    return company_balance

def calculate_office_balance(office):
    office_balance = 0
    cashbox = OfficeCashbox.objects.get(office=office)
    office_balance += float(cashbox.balance)
    return office_balance

def cashflow_create(
    holding=None, 
    company=None, 
    office=None, 
    date=datetime.date.today(), 
    operation_style=None, 
    description=None, 
    initial_balance=0, 
    subsequent_balance=0, 
    quantity=0, 
    executor=None,
    holding_initial_balance=0,
    holding_subsequent_balance=0,
    company_initial_balance=0,
    company_subsequent_balance=0,
    office_initial_balance=0,
    office_subsequent_balance=0,
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
        initial_balance=initial_balance,
        subsequent_balance=subsequent_balance,
        executor=executor,
        holding_initial_balance=holding_initial_balance,
        holding_subsequent_balance=holding_subsequent_balance,
        company_initial_balance=company_initial_balance,
        company_subsequent_balance=company_subsequent_balance,
        office_initial_balance=office_initial_balance,
        office_subsequent_balance=office_subsequent_balance,
        quantity=quantity
    )
    return cashflow.save()