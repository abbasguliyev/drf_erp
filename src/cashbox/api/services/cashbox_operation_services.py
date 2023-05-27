from cashbox.models import (
    HoldingCashboxOperation, 
    CompanyCashboxOperation,
)
from rest_framework.exceptions import ValidationError
import datetime
from cashbox.api.utils import (
    cashflow_create, 
)
from cashbox import INCOME, EXPENSE
from company.models import Holding
from cashbox.api.selectors import (
    holding_cashbox_list,
    company_cashbox_list,
    office_cashbox_list,
)
from company.api.selectors import holding_list, company_list, office_list, department_list, section_list

from django.contrib.auth import get_user_model

User = get_user_model()

def holding_cashbox_operation_create(
    *, executor=None,
    personal = None,
    amount: float, 
    note: str = None,
    operation = INCOME,
    cost_type = None,
    customer = None,
    date = datetime.date.today()
) -> HoldingCashboxOperation:
    if amount is not None:
        amount = float(amount)
    
    holding = holding_list().filter().last()
    if holding is None:
        raise ValidationError({"detail": "Holdinq məlumatları əlavə edilməyib"})

    holding_cashbox = holding_cashbox_list().last()
    if holding_cashbox is None:
        raise ValidationError({"detail": "Holdinq kassa tapılmadı"})
    
    balance = 0

    if operation == INCOME:            
        holding_cashbox.balance = float(holding_cashbox.balance) + amount
        holding_cashbox.save()
        
        balance = holding_cashbox.balance

        cashflow_create(
            holding=holding,
            operation_style="MƏDAXİL",
            description=note,
            executor=executor,
            personal=personal,
            date=date,
            quantity=amount,
            balance=balance,
            customer=customer,
            cost_type=cost_type
        )
    
    if operation == EXPENSE:            
        if amount > holding_cashbox.balance:
            raise ValidationError({"detail": "Məxaric məbləği kassanın balansıdan böyük ola bilməz"})
        
        holding_cashbox.balance = float(holding_cashbox.balance) - amount
        holding_cashbox.save()

        balance = holding_cashbox.balance

        cashflow_create(
            holding=holding,
            operation_style="MƏXARİC",
            description=note,
            executor=executor,
            personal=personal,
            date=date,
            quantity=amount,
            balance=balance,
            customer=customer,
            cost_type=cost_type
        )
    
    obj = HoldingCashboxOperation.objects.create(
        executor = executor,
        personal = personal,
        amount = amount,
        note = note,
        operation=operation,
        cost_type=cost_type
    )

    obj.full_clean()
    obj.save()

    return obj

def company_cashbox_operation_create(
    *, executor = None,
    personal = None,
    company,
    office = None,
    amount: float, 
    note: str = None,
    operation = INCOME,
    cost_type = None,
    customer = None,
    date = datetime.date.today()
) -> CompanyCashboxOperation:
    if company is None:
        raise ValidationError({"detail": "Şirkət daxil edilməyib"})
    
    if amount is not None:
        amount = float(amount)

    balance = 0
    cashbox = None

    if office is not None:
        cashbox = office_cashbox_list().filter(office=office).last()
        if cashbox is None:
            raise ValidationError({"detail": "Ofis kassa tapılmadı"})
    else:
        cashbox = company_cashbox_list().filter(company=company).last()
        if cashbox is None:
            raise ValidationError({"detail": "Şirkət kassa tapılmadı"})

    if operation == INCOME:            
        cashbox.balance = float(cashbox.balance) + amount
        cashbox.save()

        balance = cashbox.balance
        
        cashflow_create(
            office=office,
            company=company,
            operation_style="MƏDAXİL",
            description=note,
            executor=executor,
            personal=personal,
            date=date,
            quantity=amount,
            balance=balance,
            customer=customer,
            cost_type=cost_type
        )
    
    if operation == EXPENSE:            
        if amount > cashbox.balance:
            raise ValidationError({"detail": "Məxaric məbləği kassanın balansıdan böyük ola bilməz"})
        
        cashbox.balance = float(cashbox.balance) - amount
        cashbox.save()

        balance = cashbox.balance
            
        cashflow_create(
            office=office,
            company=company,
            operation_style="MƏXARİC",
            description=note,
            executor=executor,
            personal=personal,
            date=date,
            quantity=amount,
            balance=balance,
            customer=customer,
            cost_type=cost_type
        )
    
    obj = CompanyCashboxOperation.objects.create(
        executor = executor,
        personal = personal,
        amount = amount,
        note = note,
        company = company,
        office = office,
        operation=operation,
        cost_type=cost_type
    )

    obj.full_clean()
    obj.save()

    return obj