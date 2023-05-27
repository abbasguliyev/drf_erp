import datetime
from rest_framework.exceptions import ValidationError
from company.models import Holding
from company.api.selectors import holding_list
from salary.models import SalaryView
from salary.api.selectors import salary_view_list
from cashbox.api.services.cashbox_operation_services import company_cashbox_operation_create, holding_cashbox_operation_create
from cashbox import EXPENSE, INCOME
from contract.api.selectors import installment_list

def cashbox_operation_decorator(func):
    """
    Əməliyyat zamanı kassadan pul məxaric(mədaxil) edən və pul axını səhifəsinə əməliyyat ilə bağlı məlumatlar əlavə
    edilən funksiyalarda istifadə olunmalı olan dekorator funksiyası.
    Kassadan pul məxaric(mədaxil) edilməsini və pul axını səhifəsinə məlumatların əlavə edilməsini təmin edir.
    """
    def wrapper(*args, **kwargs):
        try:
            func_name = kwargs['func_name']
        except:
            func_name = None
        try:
            operation = kwargs['operation']
        except:
            operation = EXPENSE
            
        if func_name == "salary_pay_create":
            salary_view = kwargs.get('salary_view')
            employee = salary_view.employee
            date = salary_view.date
            note = salary_view.note
            executor = kwargs.get('executor')
        elif func_name == "cash_contract":
            executor = kwargs.get('user')
            date = kwargs.get('contract_date')
            instance_note = kwargs.get('note')
            if instance_note is None:
                instance_note = ""
            note = f'Nəğd satış. {instance_note}'
            employee = None
            operation = INCOME
        elif func_name == "installment_contract":
            executor = kwargs.get('user')
            date = kwargs.get('contract_date')
            instance_note = kwargs.get('note')
            if instance_note is None:
                instance_note = ""
            note = f'Kredit ilə satış ilkin ödəniş. {instance_note}'
            employee = None
            operation = INCOME
        elif func_name == "change_contract":
            executor = kwargs.get('group_leader')
            date = kwargs.get('contract_date')
            note = kwargs.get('note')
            employee = None
            operation = INCOME
            return func(*args, **kwargs)
        elif func_name == "contract_gift":
            executor = kwargs.get('user')
            date = kwargs.get('date')
            note = kwargs.get('note')
            employee = None
            operation = INCOME
        elif func_name == "finish_debt":
            executor = kwargs.get('user')
            installment = kwargs.get('installment')
            date = datetime.date.today()
            instance_note = kwargs.get('note')
            if instance_note is None:
                instance_note = ""
            note = f"Borcu bağla əməliyyatı. {instance_note}"
            employee = None
            operation = INCOME
        elif func_name == "pay_initial_payment_debt":
            executor = kwargs.get('user')
            contract = kwargs.get('contract')
            date = datetime.date.today()
            note = f"Qalıq ilkin ödəniş"
            employee = None
            operation = INCOME
        elif func_name == "incomplete_payment":
            executor = kwargs.get('user')
            installment = kwargs.get('installment')
            date = datetime.date.today()
            instance_note = kwargs.get('note')
            if instance_note is None:
                instance_note = ""
            note = f"Natamam ödəmə. {instance_note}"
            employee = None
            operation = INCOME
        elif func_name == "overpayment_installment":
            executor = kwargs.get('user')
            installment = kwargs.get('installment')
            date = datetime.date.today()
            instance_note = kwargs.get('note')
            if instance_note is None:
                instance_note = ""
            note = f"Artıq ödəmə. {instance_note}"
            employee = None
            operation = INCOME
        elif func_name == "pay_installment":
            executor = kwargs.get('user')
            installment = kwargs.get('installment')
            date = datetime.date.today()
            note = f"Kredit ödənişi"
            employee = None
            operation = INCOME
        elif func_name == "compensation_income_func":
            executor = kwargs.get('user')
            contract = kwargs.get('contract')
            date = datetime.date.today()
            instance_note = kwargs.get("note")
            if instance_note is None:
                instance_note = ""
            note = f'Söküntü. {instance_note}'
            employee = None
            operation = INCOME
        elif func_name == "compensation_expense_func":
            executor = kwargs.get('user')
            contract = kwargs.get('contract')
            date = datetime.date.today()
            instance_note = kwargs.get("note")
            if instance_note is None:
                instance_note = ""
            note = f'Söküntü. {instance_note}'
            employee = None
            operation = EXPENSE
        elif func_name == "pay_service_initial_payment":
            executor = kwargs.get('employee')
            service = kwargs.get('service')
            date = datetime.date.today()
            note = f"Servisin ilkin ödənişi"
            employee = None
            operation = INCOME
        else:
            employee = kwargs.get('employee')
            date = kwargs.get('date')
            note = kwargs.get('note')
            executor = kwargs.get('executor')

        now = datetime.date.today()
        if func_name != "salary_pay_create":
            if date is None:
                raise ValidationError({"detail": "Tarixi daxil edin"})

            if date is not None and date.year <= now.year and date.month < now.month:
                raise ValidationError({"detail": "Tarixi doğru daxil edin. Keçmiş tarix daxil edilə bilməz"})

            if date is not None and date.year >= now.year and date.month > now.month:
                raise ValidationError({"detail": "Tarixi doğru daxil edin. Gələcək tarix daxil edilə bilməz"})
        
        if func_name == "salary_pay_create":
            salary_view = kwargs.get('salary_view')
            amount = salary_view.final_salary
        elif func_name == "cash_contract":
            amount = kwargs.get('total_price')
        elif func_name == "installment_contract":
            initial_payment = kwargs.get('initial_payment')
            if initial_payment is not None:
                amount = initial_payment
            else:
                amount = 0
                obj = func(*args, **kwargs)
                return obj
        elif func_name == "finish_debt":
            contract = installment.contract
            unpaid_installments = installment_list().filter(contract=contract, payment_status="ÖDƏNMƏYƏN")
            amount_for_month = 0
            for unpaid_installment in unpaid_installments:
                amount_for_month = amount_for_month + unpaid_installment.price
            amount = amount_for_month
        elif func_name == "incomplete_payment" or func_name=="overpayment_installment":
            amount = kwargs.get('amount_wants_to_pay')
        elif func_name == "pay_installment":
            installment = kwargs.get('installment')
            amount = installment.price
        elif func_name == "pay_initial_payment_debt":
            amount = kwargs.get('initial_payment_amount')
        elif func_name == "compensation_income_func":
            amount = kwargs.get('compensation_income')
        elif func_name == "compensation_expense_func":
            amount = kwargs.get('compensation_expense')
        else:
            amount = kwargs.get('amount')

        if func_name == "cash_contract" or func_name == "installment_contract" or func_name == "contract_gift":
            office = kwargs.get('office')
            company = kwargs.get('company')
            holding = holding_list().first()
            customer = kwargs.get('customer')
        elif func_name == "incomplete_payment" or func_name=="overpayment_installment" or func_name == "pay_installment" or func_name == "finish_debt":
            installment = kwargs.get('installment')
            office = installment.contract.office
            company = installment.contract.company
            holding = holding_list().first()
            customer = installment.contract.customer
        elif func_name == "pay_initial_payment_debt" or func_name == "compensation_income_func" or func_name == "compensation_expense_func":
            contract = kwargs.get('contract')
            office = contract.office
            company = contract.company
            holding = holding_list().first()
            customer = contract.customer
        elif func_name == "pay_service_initial_payment":
            office = None
            company = None
            holding = holding_list().first()
            customer = None
        else:
            office = executor.office
            company = executor.company
            holding = holding_list().first()
            customer = None

        if operation == INCOME:
            obj = func(*args, **kwargs)

        if office is not None:
            company_cashbox_operation_create(executor=executor, personal=employee, company=company, office=office, amount=amount, note=note, operation=operation, customer=customer)
        elif office is None and company is not None:
            company_cashbox_operation_create(executor=executor, personal=employee, company=company, amount=amount, note=note, operation=operation, customer=customer)
        elif office is None and company is None and holding is not None:
            holding_cashbox_operation_create(executor=executor, personal=employee, amount=amount, note=note, operation=operation, customer=customer)

        if operation == EXPENSE:
            obj = func(*args, **kwargs)

        return obj

    return wrapper