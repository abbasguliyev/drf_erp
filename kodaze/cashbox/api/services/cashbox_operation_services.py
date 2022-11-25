from cashbox.models import (
    HoldingCashboxOperation, 
    CompanyCashboxOperation, 
    HoldingCashbox, 
    CompanyCashbox, 
    OfficeCashbox
)
from rest_framework.exceptions import ValidationError
import datetime
from cashbox.api.utils import (
    calculate_holding_total_balance, 
    cashflow_create, 
    calculate_office_balance, 
    calculate_company_balance, 
    calculate_holding_balance
)
from cashbox import INCOME, EXPENSE
from company.models import Holding
from cashbox.api.selectors import (
    holding_cashbox_list,
    company_cashbox_list,
    office_cashbox_list,
    cash_flow_list,
    holding_cashbox_opr_list,
    company_cashbox_opr_list
)
from django.contrib.auth import get_user_model

User = get_user_model()

def holding_cashbox_operation_create(
    *, executor,
    personal = None,
    amount: float, 
    note: str = None,
    operation = INCOME
) -> HoldingCashboxOperation:
    holding = Holding.objects.filter().last()
    if holding is None:
        raise ValidationError({"detail": "Holdinq məlumatları əlavə edilməyib"})

    holding_cashbox = holding_cashbox_list().last()
    if holding_cashbox is None:
        raise ValidationError({"detail": "Holdinq kassa tapılmadı"})
    
    balance = 0

    if operation == INCOME:            
        holding_cashbox.balance = holding_cashbox.balance + amount
        holding_cashbox.save()
        
        balance = holding_cashbox.balance

        cashflow_create(
            holding=holding,
            operation_style="MƏDAXİL",
            description=f"{holding.name} holdinq kassasına {float(amount)} AZN mədaxil edildi",
            executor=executor,
            personal=personal,
            date=datetime.date.today(),
            quantity=float(amount),
            balance=balance
        )
    
    if operation == EXPENSE:            
        if amount > holding_cashbox.balance:
            raise ValidationError({"detail": "Məxaric məbləği kassanın balansıdan böyük ola bilməz"})
        
        holding_cashbox.balance = holding_cashbox.balance - amount
        holding_cashbox.save()

        balance = holding_cashbox.balance

        cashflow_create(
            holding=holding,
            operation_style="MƏXARİC",
            description=f"{holding.name} holdinq kassasından {float(amount)} AZN məxaric edildi",
            executor=executor,
            personal=personal,
            date=datetime.date.today(),
            quantity=float(amount),
            balance=balance
        )
    
    obj = HoldingCashboxOperation.objects.create(
        executor = executor,
        personal = personal,
        amount = amount,
        note = note,
        operation=operation
    )

    obj.full_clean()
    obj.save()

    return obj

def company_cashbox_operation_create(
    *, executor,
    personal = None,
    company,
    office = None,
    amount: float, 
    note: str = None,
    operation = INCOME
) -> CompanyCashboxOperation:
    if company is None:
        raise ValidationError({"detail": "Şirkət daxil edilməyib"})

    balance = 0
    cashbox = None

    if office is not None:
        cashbox = office_cashbox_list().filter(office=office).last()
        if cashbox is None:
            raise ValidationError({"detail": "Ofis kassa tapılmadı"})
        if note is None:
            description_income=f"{office.name} ofis kassasına {float(amount)} AZN mədaxil edildi"
            description_expense=f"{office.name} ofis kassasından {float(amount)} AZN məxaric edildi"
        else:
            description_income=note
            description_expense=note
    else:
        cashbox = company_cashbox_list().last()
        if cashbox is None:
            raise ValidationError({"detail": "Şirkət kassa tapılmadı"})
        if note is None:
            description_income=f"{company.name} şirkət kassasına {float(amount)} AZN mədaxil edildi"
            description_expense=f"{company.name} şirkət kassasından {float(amount)} AZN məxaric edildi"
        else:
            description_income=note
            description_expense=note

    if operation == INCOME:            
        cashbox.balance = cashbox.balance + amount
        cashbox.save()

        balance = cashbox.balance
        
        cashflow_create(
            office=office,
            company=office.company,
            operation_style="MƏDAXİL",
            description=description_income,
            executor=executor,
            personal=personal,
            date=datetime.date.today(),
            quantity=float(amount),
            balance=balance
        )
    
    if operation == EXPENSE:            
        if amount > cashbox.balance:
            raise ValidationError({"detail": "Məxaric məbləği kassanın balansıdan böyük ola bilməz"})
        
        cashbox.balance = cashbox.balance - amount
        cashbox.save()

        balance = cashbox.balance
            
        cashflow_create(
            office=office,
            company=office.company,
            operation_style="MƏXARİC",
            description=description_expense,
            executor=executor,
            personal=personal,
            date=datetime.date.today(),
            quantity=float(amount),
            balance=balance
        )
    
    obj = CompanyCashboxOperation.objects.create(
        executor = executor,
        personal = personal,
        amount = amount,
        note = note,
        company = company,
        office = office,
        operation=operation
    )

    obj.full_clean()
    obj.save()

    return obj