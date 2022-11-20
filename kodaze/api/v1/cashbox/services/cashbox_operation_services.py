from cashbox.models import (
    HoldingCashboxOperation, 
    CompanyCashboxOperation, 
    HoldingCashbox, 
    CompanyCashbox, 
    OfficeCashbox
)
from rest_framework.exceptions import ValidationError
import datetime
from api.v1.cashbox.utils import (
    calculate_holding_total_balance, 
    cashflow_create, 
    calculate_office_balance, 
    calculate_company_balance, 
    calculate_holding_balance
)
from cashbox import INCOME, EXPENSE
from company.models import Holding
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

    holding_cashbox = HoldingCashbox.objects.filter().last()
    if holding_cashbox is None:
        raise ValidationError({"detail": "Holdinq kassa tapılmadı"})

    initial_balance = calculate_holding_total_balance()
    holding_initial_balance = calculate_holding_balance()

    if operation == INCOME:            
        holding_cashbox.balance = holding_cashbox.balance + amount
        holding_cashbox.save()
        
        subsequent_balance = calculate_holding_total_balance()
        holding_subsequent_balance = calculate_holding_balance()
        
        cashflow_create(
            holding=holding,
            operation_style="MƏDAXİL",
            description=f"{holding.name} holdinq kassasına {float(amount)} AZN mədaxil edildi",
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            holding_initial_balance=holding_initial_balance,
            holding_subsequent_balance=holding_subsequent_balance,
            executor=executor,
            personal=personal,
            date=datetime.date.today(),
            quantity=float(amount)
        )
    
    if operation == EXPENSE:            
        if amount > holding_cashbox.balance:
            raise ValidationError({"detail": "Məxaric məbləği kassanın balansıdan böyük ola bilməz"})
        
        holding_cashbox.balance = holding_cashbox.balance - amount
        holding_cashbox.save()

        subsequent_balance = calculate_holding_total_balance()
        holding_subsequent_balance = calculate_holding_balance()

        cashflow_create(
            holding=holding,
            operation_style="MƏXARİC",
            description=f"{holding.name} holdinq kassasından {float(amount)} AZN məxaric edildi",
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            holding_initial_balance=holding_initial_balance,
            holding_subsequent_balance=holding_subsequent_balance,
            executor=executor,
            personal=personal,
            date=datetime.date.today(),
            quantity=float(amount)
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

    initial_balance = calculate_holding_total_balance()
    office_initial_balance = 0
    company_initial_balance = 0
    cashbox = None

    if office is not None:
        cashbox = OfficeCashbox.objects.filter(office=office).last()
        if cashbox is None:
            raise ValidationError({"detail": "Ofis kassa tapılmadı"})
        office_initial_balance = calculate_office_balance(office=office)
        description_income=f"{office.name} ofis kassasına {float(amount)} AZN əlavə edildi"
        description_expense=f"{office.name} ofis kassasından {float(amount)} AZN məxaric edildi"
    else:
        cashbox = CompanyCashbox.objects.filter(company=company).last()
        if cashbox is None:
            raise ValidationError({"detail": "Şirkət kassa tapılmadı"})
        company_initial_balance = calculate_company_balance(company=company)
        description_income=f"{company.name} şirkət kassasına {float(amount)} AZN əlavə edildi"
        description_expense=f"{company.name} şirkət kassasından {float(amount)} AZN məxaric edildi"

    if operation == INCOME:            
        cashbox.balance = cashbox.balance + amount
        cashbox.save()
        
        subsequent_balance = calculate_holding_total_balance()
        if office is not None:
            office_subsequent_balance = calculate_office_balance(office=office)
        else:
            office_subsequent_balance = 0
        
        if company is not None:
            company_subsequent_balance = calculate_company_balance(company=company)
        else:
            company_subsequent_balance = 0

        cashflow_create(
            office=office,
            company=office.company,
            operation_style="MƏDAXİL",
            description=description_income,
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            company_initial_balance = company_initial_balance, 
            company_subsequent_balance = company_subsequent_balance,
            office_initial_balance=office_initial_balance,
            office_subsequent_balance=office_subsequent_balance,
            executor=executor,
            personal=personal,
            date=datetime.date.today(),
            quantity=float(amount)
        )
    
    if operation == EXPENSE:            
        if amount > cashbox.balance:
            raise ValidationError({"detail": "Məxaric məbləği kassanın balansıdan böyük ola bilməz"})
        
        cashbox.balance = cashbox.balance - amount
        cashbox.save()

        subsequent_balance = calculate_holding_total_balance()
        if office is not None:
            office_subsequent_balance = calculate_office_balance(office=office)
        else:
            office_subsequent_balance = 0
        
        if company is not None:
            company_subsequent_balance = calculate_company_balance(company=company)
        else:
            company_subsequent_balance = 0
            
        cashflow_create(
            office=office,
            company=office.company,
            operation_style="MƏXARİC",
            description=description_expense,
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            company_initial_balance = company_initial_balance, 
            company_subsequent_balance = company_subsequent_balance,
            office_initial_balance=office_initial_balance,
            office_subsequent_balance=office_subsequent_balance,
            executor=executor,
            personal=personal,
            date=datetime.date.today(),
            quantity=float(amount)
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