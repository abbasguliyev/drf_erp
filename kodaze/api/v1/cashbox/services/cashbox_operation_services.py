from cashbox.models import (
    HoldingCashboxOperation, 
    OfficeCashboxOperation, 
    HoldingCashbox, 
    CompanyCashbox, 
    OfficeCashbox
)
from cashbox import INCOME, EXPENSE
from rest_framework.exceptions import ValidationError
import datetime
from api.v1.cashbox.utils import (
    calculate_holding_total_balance, 
    cashflow_create, 
    calculate_office_balance, 
    calculate_company_balance, 
    calculate_holding_balance
)

from company.models import Holding, Company, Office

def holding_cashbox_operation_create(
    *, executor,
    amount: float, 
    note: str = None,
    operation: str = INCOME
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
            date=datetime.date.today(),
            quantity=float(amount)
        )
    
    obj = HoldingCashboxOperation.objects.create(
        executor = executor,
        amount = amount,
        note = note
    )

    obj.full_clean()
    obj.save()

    return obj

def office_cashbox_operation_create(
    *, executor,
    company,
    office,
    amount: float, 
    note: str = None,
    operation: str = INCOME
) -> HoldingCashboxOperation:
    if company is None:
        raise ValidationError({"detail": "Şirkət daxil edilməyib"})

    if office is None:
        raise ValidationError({"detail": "Ofis daxil edilməyib"})

    office_cashbox = OfficeCashbox.objects.filter(office=office).last()
    if office_cashbox is None:
        raise ValidationError({"detail": "Ofis kassa tapılmadı"})

    initial_balance = calculate_holding_total_balance()
    office_initial_balance = calculate_office_balance(office=office)

    if operation == INCOME:            
        office_cashbox.balance = office_cashbox.balance + amount
        office_cashbox.save()
        
        subsequent_balance = calculate_holding_total_balance()
        office_subsequent_balance = calculate_office_balance(office=office)

        cashflow_create(
            office=office,
            company=office.company,
            operation_style="MƏDAXİL",
            description=f"{office.name} ofis kassasına {float(amount)} AZN əlavə edildi",
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            office_initial_balance=office_initial_balance,
            office_subsequent_balance=office_subsequent_balance,
            executor=executor,
            date=datetime.date.today(),
            quantity=float(amount)
        )
    
    if operation == EXPENSE:            
        if amount > office_cashbox.balance:
            raise ValidationError({"detail": "Məxaric məbləği kassanın balansıdan böyük ola bilməz"})
        
        office_cashbox.balance = office_cashbox.balance - amount
        office_cashbox.save()

        subsequent_balance = calculate_holding_total_balance()
        office_subsequent_balance = calculate_office_balance(office=office)
        cashflow_create(
            office=office,
            company=office.company,
            operation_style="MƏXARİC",
            description=f"{office.name} ofis kassasından {float(amount)} AZN məxaric edildi",
            initial_balance=initial_balance,
            subsequent_balance=subsequent_balance,
            office_initial_balance=office_initial_balance,
            office_subsequent_balance=office_subsequent_balance,
            executor=executor,
            date=datetime.date.today(),
            quantity=float(amount)
        )
    
    obj = OfficeCashboxOperation.objects.create(
        executor = executor,
        amount = amount,
        note = note,
        company = company,
        office = office
    )

    obj.full_clean()
    obj.save()

    return obj