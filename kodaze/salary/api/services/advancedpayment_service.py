import datetime
from rest_framework.exceptions import ValidationError
from salary.models import AdvancePayment
from salary.api.decorators import add_amount_to_salary_view_decorator
from cashbox.api.decorators import cashbox_operation_decorator
from salary.api.selectors import (
    advance_payment_list,
)


@cashbox_operation_decorator
@add_amount_to_salary_view_decorator
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

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})
    
    if (amount == None):
        raise ValidationError({"detail": "Məbləği daxil edin"})

    user_advanced_payment = advance_payment_list().filter(employee=employee, salary_date__year=f"{salary_date.year}", salary_date__month=f"{salary_date.month}").count()
    if user_advanced_payment >= 2:
        raise ValidationError({"detail": "Bir işçiyə eyni ay ərzində maksimum 2 dəfə avans verilə bilər"})

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

    return advance_payment
