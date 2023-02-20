import datetime
from rest_framework.exceptions import ValidationError
from salary.models import AdvancePayment
from salary.api.selectors import advance_payment_list, salary_view_list
from salary.api.services.employee_activity_service import employee_activity_history_create
from salary.api.utils import salary_operation_delete
import pandas as pd
from cashbox.api.services.cashbox_operation_services import company_cashbox_operation_create, holding_cashbox_operation_create
from company.models import Holding
from cashbox import EXPENSE
from company.api.selectors import holding_list, company_list, office_list, section_list, department_list


def advancepayment_create(
        executor,
        employee,
        amount: float = None,
        note: str = None,
        date: datetime.date = None,
        salary_date: datetime.date = None
) -> AdvancePayment:
    """
    İşçiyə avans vermə funksiyası
    """
    now = datetime.date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    previous_month = d - pd.offsets.MonthBegin(1)

    previous_month_salary_view = salary_view_list().filter(employee=employee, date=f"{previous_month.year}-{previous_month.month}-{1}").last()
    
    try:
        if previous_month_salary_view is not None and previous_month_salary_view.is_paid == False:
            salary_view = previous_month_salary_view
        else:
            current_salary_view = salary_view_list().filter(employee=employee, date=f"{now.year}-{now.month}-{1}").last()
            if current_salary_view.is_paid == False:
                salary_view = current_salary_view
            else:
                raise ValidationError({'detail': 'Ə/H artıq ödənilib'})
    except ValidationError as err:
        raise err

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})
    
    if (amount == None):
        raise ValidationError({"detail": "Məbləği daxil edin"})

    user_advanced_payment = advance_payment_list().filter(employee=employee, salary_date__year=f"{date.year}", date__month=f"{date.month}").count()
    if user_advanced_payment >= 2:
        raise ValidationError({"detail": "Bir işçiyə eyni ay ərzində maksimum 2 dəfə avans verilə bilər"})
    
    thirty_per_cent_of_final_salary = (salary_view.final_salary * 30) / 100
    
    if amount is None:
        amount = thirty_per_cent_of_final_salary
    else:
        if amount > thirty_per_cent_of_final_salary:
            raise ValidationError({"detail": "Verilən avans yekun məbləğin 30% miqdarında olmalıdır."})
        else:
            amount = amount
    
    if salary_date is None:
        salary_date = salary_view.date
    
    if amount > salary_view.final_salary:
        raise ValidationError({"detail": "Daxil edilmiş məbləği işçinin yekun maaşından çox ola bilməz"})
    
    process_description = f"{employee.fullname} avans əməliyyatı" 

    salary_view.final_salary = salary_view.final_salary - amount
    salary_view.save()

    operation = EXPENSE
    office = employee.office
    company = employee.company
    holding = holding_list().first()

    if office is not None:
        company_cashbox_operation_create(executor=executor, personal=employee, company=company, office=office, amount=amount, note=process_description, operation=operation)
    elif office is None and company is not None:
        company_cashbox_operation_create(executor=executor, personal=employee, company=company, amount=amount, note=process_description, operation=operation)
    elif office is None and company is None and holding is not None:
        holding_cashbox_operation_create(executor=executor, personal=employee, amount=amount, note=process_description, operation=operation)
    
    advance_payment = AdvancePayment.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date,
        is_paid=True,
        salary_date=salary_date
    )
    advance_payment.full_clean()
    advance_payment.save()
    
    employee_activity_history_create(
        salary_view = salary_view,
        func_name = "advancepayment_create",
        amount = amount
    )

    return advance_payment

def advance_payment_update(instance, **data):
    obj = advance_payment_list().filter(id=instance.id).update(**data)
    return obj


def advance_payment_delete(instance_list_id, func_name=None):
    for instance in instance_list_id:
        if instance.is_paid == True:
            continue
        salary_operation_delete(instance=instance, func_name=func_name)