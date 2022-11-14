from salary.models import SalaryView
from datetime import date


def salary_view_create(
    *, employee,
    sale_quantity: int = 0,
    sales_amount: float = 0,
    amount: float = 0,
    note: str = None,
    final_salary: float = 0,
    date: date = date.today(),
    commission_amount: float = 0
) -> SalaryView:
    obj = SalaryView.objects.create(
        employee=employee,
        sale_quantity=sale_quantity,
        sales_amount=sales_amount,
        amount=amount,
        note=note,
        final_salary=final_salary,
        date=date,
        commission_amount=commission_amount
    )

    obj.full_clean()
    obj.save()

    return obj
