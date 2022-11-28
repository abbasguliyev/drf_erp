import datetime
from cashbox.api.decorators import cashbox_operation_decorator
from salary.models import PaySalary
from rest_framework.exceptions import ValidationError
from salary.api.selectors import (
    salary_deduction_list,
    salary_punishment_list,
    bonus_list
)

def salary_pay_service(executor, salary_view) -> PaySalary:
    if salary_view is None:
        raise ValidationError({"detail": "Əməliyyatı icra etmək üçün əməkhaqqı cədvəlindən kimlərin əməkhaqqısının ödəniləcəyi seçilməlidir"})
    for sw in salary_view:
        salary_pay_create(executor=executor, salary_view=sw, func_name='salary_pay_create')
    
@cashbox_operation_decorator
def salary_pay_create(executor, salary_view, func_name):
    now = datetime.date.today()
    sw = salary_view

    employee = sw.employee
    sw.final_salary = 0
    sw.is_done = True
    sw.is_paid = True
    sw.pay_date = now
    sw.save()

    all_bonus = bonus_list().filter(employee=employee, salary_date__month=salary_view.date.month, salary_date__year=salary_view.date.year) 
    all_sd = salary_deduction_list().filter(employee=employee, salary_date__month=salary_view.date.month, salary_date__year=salary_view.date.year).filter()
    all_sp = salary_punishment_list().filter(employee=employee, salary_date__month=salary_view.date.month, salary_date__year=salary_view.date.year)

    for b in all_bonus:
        b.is_paid = True
        b.save()
    for sd in all_sd:
        sd.is_paid = True
        sd.save()
    for sp in all_sp:
        sp.is_paid = True
        sp.save()
