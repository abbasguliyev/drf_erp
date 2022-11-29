from salary.models import EmployeeActivityHistory
from salary.api.selectors import employee_activity_history_list

def employee_activity_history_create(
    *, salary_view,
    func_name = None,
    amount,
    bonus: float = 0,
    advance_payment: float = 0,
    salary_deduction: float = 0,
    salary_punishment: float = 0
):
    if func_name == 'advancepayment_create':
        advance_payment = amount
    else:
        advance_payment = 0

    if func_name == 'bonus_create':
        bonus = amount
    else:
        bonus = 0

    if func_name == 'salarydeduction_create':
        salary_deduction = amount
    else:
        salary_deduction = 0

    if func_name == 'salarypunishment_create':
        salary_punishment = amount
    else:
        salary_punishment = 0
    month = salary_view.date.month
    year = salary_view.date.year
    obj = employee_activity_history_list().filter(salary_view=salary_view, activity_date__month=month, activity_date__year=year).last()
    if obj is None:
        new_obj = EmployeeActivityHistory.objects.create(
            salary_view=salary_view,
            bonus=bonus,
            advance_payment=advance_payment,
            salary_deduction=salary_deduction,
            salary_punishment=salary_punishment,
            activity_date=salary_view.date
        )
        new_obj.full_clean()
        new_obj.save()
    else:
        obj.advance_payment = obj.advance_payment + advance_payment 
        obj.bonus = obj.bonus + bonus 
        obj.salary_deduction = obj.salary_deduction + salary_deduction 
        obj.salary_punishment = obj.salary_punishment + salary_punishment 
        obj.save()