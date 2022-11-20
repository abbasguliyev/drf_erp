import datetime
from salary.models import Bonus
from rest_framework.exceptions import ValidationError
from api.v1.salary.decorators import add_amount_to_salary_view_decorator

@add_amount_to_salary_view_decorator
def bonus_create(
        *, employee,
        amount: float = None,
        note: str = None,
        date: datetime.date = None
) -> Bonus:
    """
    İşçilərə bonus vermək funksiyası
    """

    if (date == None):
        raise ValidationError({"detail": "Tarixi daxil edin"})

    if (amount == None):
        raise ValidationError({"detail": "Məbləği daxil edin"})
    
    bonus = Bonus.objects.create(
        employee=employee,
        amount=amount,
        note=note,
        date=date
    )

    bonus.full_clean()
    bonus.save()

    return bonus
