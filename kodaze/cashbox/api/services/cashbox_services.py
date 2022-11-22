from cashbox.models import Cashbox, HoldingCashbox, OfficeCashbox, CompanyCashbox
from company.models import Holding, Office, Company
from cashbox.api.selectors import (
    holding_cashbox_list,
    company_cashbox_list,
    office_cashbox_list,
    cash_flow_list,
    holding_cashbox_opr_list,
    company_cashbox_opr_list
)

def update_cashbox_service(instance, **data) -> Cashbox:
    obj = instance.update(**data)
    return obj

def create_office_cashbox_service(
    *, title: str = None,
    balance: float = 0,
    note: str = None,
    office: Office
) -> OfficeCashbox:
    office_cashbox = office_cashbox_list(filters={'office': office}).count()
    if office_cashbox == 0:
        balance = 0
        if title is None:
            title = f"{office.name}({office.company.name}) ofisinin anbarı"
        office_cashbox = OfficeCashbox.objects.create(title=title, office=office, balance=balance, note=note)
        office_cashbox.full_clean()
        office_cashbox.save()
    
    return office_cashbox

def create_company_cashbox_service(
    *, title: str = None,
    balance: float = 0,
    note: str = None,
    company: Company
) -> CompanyCashbox:
    company_cashbox = company_cashbox_list(filters={'company': company}).count()
    if company_cashbox == 0:
        balance = 0
        if title is None:
            title = f"{company.name} şirkətinin anbarı"
        company_cashbox = CompanyCashbox.objects.create(title=title, company=company, balance=balance, note=note)
        company_cashbox.full_clean()
        company_cashbox.save()
        
    return company_cashbox

def create_holding_cashbox_service(
    *, title: str = None,
    balance: float = 0,
    note: str = None,
    holding: Holding
) -> HoldingCashbox:
    holding_cashbox = holding_cashbox_list(filters={'holding': holding}).count()
    if holding_cashbox == 0:
        balance = 0
        if title is None:
            title = f"{holding.name} holdinqinin anbarı"
        holding_cashbox = HoldingCashbox.objects.create(title=title, holding=holding, balance=balance, note=note)
        holding_cashbox.full_clean()
        holding_cashbox.save()
    
    return holding_cashbox