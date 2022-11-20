import datetime
from rest_framework.exceptions import ValidationError
from salary.models import AdvancePayment
from api.v1.salary.decorators import add_amount_to_salary_view_decorator

@add_amount_to_salary_view_decorator
def advancepayment_create(
        executor,
        employee,
        amount: float = None,
        note: str = None,
        date: datetime.date = None
) -> AdvancePayment:
    """
    İşçiyə avans vermə funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})
    
    if (amount == None):
        raise ValidationError({"detail": "Məbləği daxil edin"})

    user_advanced_payment = AdvancePayment.objects.filter(employee=employee, date__year=f"{date.year}", date__month=f"{date.month}").count()
    if user_advanced_payment > 2:
        raise ValidationError({"detail": "Bir işçiyə eyni ay ərzində maksimum 2 dəfə avans verilə bilər"})

    advance_payment = AdvancePayment.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date,
        is_paid=True
    )
    advance_payment.full_clean()
    advance_payment.save()

    return advance_payment
