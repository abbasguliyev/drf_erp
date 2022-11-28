from company.models import Holding
from rest_framework.exceptions import ValidationError
from salary.models import SalaryView
import datetime
from cashbox.api.services.cashbox_operation_services import company_cashbox_operation_create, holding_cashbox_operation_create
from cashbox import EXPENSE
from salary.api.selectors import salary_view_list

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
            
        if func_name == "salary_pay_create":
            salary_view = kwargs['salary_view']
            employee = salary_view.employee
            date = salary_view.date
            note = salary_view.note
        else:
            employee = kwargs['employee']
            date = kwargs['date']
            note = kwargs['note']
            
        executor = kwargs['executor']
        # operation fieldi decoratorun yazildigi funksiyadan mutleq gonderilmelidir, INCOME ve ya EXPENSE olaraq gonderilmelidir.
        try:
            operation = kwargs['operation']
        except:
            operation = EXPENSE

        print(f"{func_name=}")

        now = datetime.date.today()
        
        if date is None:
            raise ValidationError({"detail": "Tarixi daxil edin"})

        if date is not None and date.year <= now.year and date.month < now.month:
            raise ValidationError({"detail": "Tarixi doğru daxil edin. Keçmiş tarix daxil edilə bilməz"})

        if date is not None and date.year >= now.year and date.month > now.month:
            raise ValidationError({"detail": "Tarixi doğru daxil edin. Gələcək tarix daxil edilə bilməz"})
        
        if func_name == "salary_pay_create":
            salary_view = kwargs['salary_view']
            amount = float(salary_view.final_salary)
        else:
            amount = kwargs['amount']

        office = employee.office
        company = employee.company
        holding = Holding.objects.all()[0]

        if office is not None:
            company_cashbox_operation_create(executor=executor, personal=employee, company=company, office=office, amount=amount, note=note, operation=operation)
        elif office is None and company is not None:
            company_cashbox_operation_create(executor=executor, personal=employee, company=company, amount=amount, note=note, operation=operation)
        elif office is None and company is None and holding is not None:
            holding_cashbox_operation_create(executor=executor, personal=employee, amount=amount, note=note, operation=operation)
        
        func(*args, **kwargs)

    return wrapper