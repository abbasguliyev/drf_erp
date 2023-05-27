import datetime
from rest_framework.exceptions import ValidationError
from cashbox.models import Cashbox, HoldingCashbox, OfficeCashbox, CompanyCashbox
from cashbox.api.utils import cashflow_create
from cashbox.api.selectors import (
    holding_cashbox_list,
    company_cashbox_list,
    office_cashbox_list,
)
from cashbox import EXPENSE, INCOME, KORREKSIYA
from company.models import Holding, Office, Company

def update_holding_cashbox_service(user, instance, **data) -> Cashbox:
    new_balance = data.get('balance')
    
    if new_balance is not None:
        before_update_balance = instance.balance
        if new_balance > before_update_balance:
            operation_style=KORREKSIYA
            difference = new_balance - before_update_balance
        elif new_balance < before_update_balance:
            operation_style=KORREKSIYA
            difference = before_update_balance - new_balance
        else:
            raise ValidationError({'detail': 'Daxil etdiyiniz məbləğ əməliyyatdan əvvəl balansda olan məbləğ ilə eynidir'})
        
        cashflow_create(
            holding=instance.holding,
            operation_style=operation_style,
            description="Korreksiya",
            executor=user,
            personal=None,
            date=datetime.date.today(),
            quantity=difference,
            balance=new_balance
        )
        
    obj = holding_cashbox_list().filter(id=instance.id).update(**data)
    return obj

def update_company_cashbox_service(user, instance, **data) -> Cashbox:
    new_balance = data.get('balance')
    
    if new_balance is not None:
        before_update_balance = instance.balance
        if new_balance > before_update_balance:
            operation_style=KORREKSIYA
            difference = new_balance - before_update_balance
        elif new_balance < before_update_balance:
            operation_style=KORREKSIYA
            difference = before_update_balance - new_balance
        else:
            raise ValidationError({'detail': 'Daxil etdiyiniz məbləğ əməliyyatdan əvvəl balansda olan məbləğ ilə eynidir'})
        
        cashflow_create(
            office=None,
            company=instance.company,
            operation_style=operation_style,
            description="Korreksiya",
            executor=user,
            personal=None,
            date=datetime.date.today(),
            quantity=difference,
            balance=new_balance
        )
    obj = company_cashbox_list().filter(id=instance.id).update(**data)
    return obj

def update_office_cashbox_service(user, instance, **data) -> Cashbox:
    new_balance = data.get('balance')
    
    if new_balance is not None:
        before_update_balance = instance.balance
        if new_balance > before_update_balance:
            operation_style=KORREKSIYA
            difference = new_balance - before_update_balance
        elif new_balance < before_update_balance:
            operation_style=KORREKSIYA
            difference = before_update_balance - new_balance
        else:
            raise ValidationError({'detail': 'Daxil etdiyiniz məbləğ əməliyyatdan əvvəl balansda olan məbləğ ilə eynidir'})
        
        cashflow_create(
            office=instance.office,
            company=instance.office.company,
            operation_style=operation_style,
            description="Korreksiya",
            executor=user,
            personal=None,
            date=datetime.date.today(),
            quantity=difference,
            balance=new_balance
        )

    obj = office_cashbox_list().filter(id=instance.id).update(**data)
    return obj

def create_office_cashbox_service(
    *, title: str = None,
    balance: float = 0,
    note: str = None,
    office: Office
) -> OfficeCashbox:
    office_cashbox = office_cashbox_list().filter(office=office).count()
    if office_cashbox == 0:
        balance = 0
        if title is None:
            title = f"{office.name}({office.company.name}) ofisinin kassası"
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
    company_cashbox = company_cashbox_list().filter(company= company).count()
    if company_cashbox == 0:
        balance = 0
        if title is None:
            title = f"{company.name} şirkətinin kassası"
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
    holding_cashbox = holding_cashbox_list().filter(holding=holding).count()
    if holding_cashbox == 0:
        balance = 0
        if title is None:
            title = f"{holding.name} holdinqinin kassası"
        holding_cashbox = HoldingCashbox.objects.create(title=title, holding=holding, balance=balance, note=note)
        holding_cashbox.full_clean()
        holding_cashbox.save()
    
    return holding_cashbox