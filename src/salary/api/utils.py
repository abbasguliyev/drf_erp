import datetime
import pandas as pd
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from contract import INSTALLMENT, CASH
from contract.api.selectors import contract_list
from salary import COUNT, FIX
from salary.models import SalaryView
from salary.api.selectors import salary_view_list
from salary.api.decorators import delete_emp_activity_history
from account.api.selectors import user_list

User = get_user_model()


def send_amount_to_salary_view(*, user: User, quantity: float=0, sale_amount: float=0, commission_amount: float=0, amount: float=0, date) -> SalaryView:
    """
    İşçi ə/h cədvəlində yekun məbləğə verilmiş məbləğin əlavə edilməsi
    """

    salary_view = salary_view_list().filter(employee=user, date= date).last()
    salary_view.sale_quantity = salary_view.sale_quantity + quantity
    salary_view.sales_amount = salary_view.sales_amount + sale_amount
    salary_view.commission_amount = salary_view.commission_amount + commission_amount
    salary_view.final_salary = salary_view.final_salary + amount
    salary_view.save()

    return salary_view

def get_back_amount_from_salary_view(user: User, amount: float, date) -> SalaryView:
    """
    İşçi ə/h cədvəlində yekun məbləğdən verilmiş məbləğin çıxılması
    """
    salary_view = salary_view_list().filter(employee=user, date= date).last()
    salary_view.final_salary = salary_view.final_salary - amount
    salary_view.save()

    return salary_view

def send_sale_quantity_to_salary_view(user: User, quantity: float, amount: float, commission_amount: float, date) -> SalaryView:
    """
    İşçi ə/h cədvəlində satış sayına verilmiş miqdarın əlavə edilməsi
    """

    salary_view = salary_view_list().filter(employee=user, date= date).last()
    salary_view.sale_quantity = salary_view.sale_quantity + quantity
    salary_view.sales_amount = salary_view.sales_amount + amount
    salary_view.commission_amount = salary_view.commission_amount + commission_amount
    salary_view.save()

    return salary_view

def get_back_sale_quantity_from_salary_view(user: User, quantity: float, amount: float, date) -> SalaryView:
    """
    İşçi ə/h cədvəlində satış sayından verilmiş miqdarın çıxılması
    """
    salary_view = salary_view_list().filter(employee=user, date= date).last()
    salary_view.sale_quantity = salary_view.sale_quantity - quantity
    salary_view.sales_amount = salary_view.sales_amount - amount
    salary_view.save()

    return salary_view


def create_fix_commission():
    """
    İşçilərə fix komissiyaların verilməsi
    """
    users = user_list().filter(is_active=True)
    now = datetime.date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)

    this_month = f"{now.year}-{now.month}-{1}"
    next_month_date = f"{next_m.year}-{next_m.month}-{1}"

    sale_range_final_salary = 0

    for user in users:
        salary_view_next_month = salary_view_list().filter(employee=user, date=next_month_date).last()
        if user.commission is not None:
            for_sale_ranges = user.commission.for_sale_range
            if for_sale_ranges.count() > 0:
                sales_quantity = salary_view_next_month.sales_quantity

                for srm in for_sale_ranges:
                    if srm.sale_type == FIX:
                        if not srm.sale_range.title.endswith("+"):
                            if int(sales_quantity) >= srm.sale_range.start_count and int(sales_quantity) <= srm.sale_range.end_count:
                                sale_range_final_salary += srm.amount
                        elif srm.sale_range.title.endswith("+"):
                            if int(sales_quantity) >= srm.sale_range.start_count:
                                sale_range_final_salary += srm.amount

            salary_view_next_month.final_salary = salary_view_next_month.final_salary + sale_range_final_salary
            salary_view_next_month.save()

def give_commission_after_contract(
        contract_id: int
):
    """
    Müqavilə imzalanarkən işçiyə təyin olunmuş komissiya üsuluna görə təyin olunmuş məbləğlərin verilməsi

    :param contract_id:
    :return:
    """
    contract = contract_list().filter(id=contract_id).last()

    now = datetime.date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)

    this_month_date = f"{now.year}-{now.month}-{1}"
    next_month_date = f"{next_m.year}-{next_m.month}-{1}"

    employee_list = list()

    group_leader = contract.group_leader
    manager1 = contract.manager1
    manager2 = contract.manager2

    if group_leader is not None:
        employee_list.append(group_leader)
    if manager1 is not None:
        employee_list.append(manager1)
    if manager2 is not None:
        employee_list.append(manager2)

    for user in employee_list:
        quantity = contract.product_quantity
        sales_amount = contract.product.price * quantity
        
        try:
            commission = user.commission
        except:
            commission = None

        if commission is not None:
            salary_view_next_month = salary_view_list().filter(employee=user, date=next_month_date).last()
            sales_quantity = salary_view_next_month.sale_quantity
            salary_view_next_month_sale_amount = salary_view_next_month.sales_amount
            salary_view_next_month_commission_amount = salary_view_next_month.commission_amount

            cash = commission.cash * contract.product_quantity
            for_team = commission.for_team * contract.product_quantity
            for_office = commission.for_office * contract.product_quantity
            
            installments = commission.installment.all()
            for_sale_ranges = commission.for_sale_range.all()
            final_salary = for_office + for_team

            contract_loan_term = contract.loan_term
            contract_payment_style = contract.payment_style

            if contract_payment_style == INSTALLMENT:
                if installments.count() > 0:
                    for inst in installments:
                        if not inst.month_range.title.endswith("+"):
                            if contract_loan_term >= inst.month_range.start_month and contract_loan_term <= inst.month_range.end_month:
                                final_salary = final_salary + (inst.amount * contract.product_quantity)
                        elif inst.month_range.title.endswith("+"):
                            if int(contract_loan_term) >= inst.month_range.start_month:
                                final_salary = final_salary + (inst.amount * contract.product_quantity)
            elif contract_payment_style == CASH:
                final_salary = final_salary + cash

            if for_sale_ranges.count() > 0:
                salary_view_n_m = salary_view_list().filter(employee=user, date= next_month_date).last()
                salary_view_n_m.sale_quantity = 0
                salary_view_n_m.sales_amount = 0
                salary_view_n_m.commission_amount = 0
                salary_view_n_m.save()
                sale_amount = 0
                for srm in for_sale_ranges:
                    if srm.sale_type == COUNT:
                        if not srm.sale_range.title.endswith("+"):
                            if srm.sale_range.end_count is not None:
                                if sales_quantity >= srm.sale_range.start_count and sales_quantity <= srm.sale_range.end_count:
                                    sale_amount = sale_amount + (sales_quantity*srm.amount)
                            else:
                                if sales_quantity == srm.sale_range.start_count:
                                    sale_amount = sale_amount + (sales_quantity*srm.amount)
                        elif srm.sale_range.title.endswith("+"):
                            if sales_quantity >= srm.sale_range.start_count:
                                sale_amount = sale_amount + (sales_quantity*srm.amount)

                salary_view_n_m.final_salary = salary_view_n_m.final_salary - sale_amount
                salary_view_n_m.save()
                salary_view_next_month_commission_amount = salary_view_next_month_commission_amount - sale_amount
                final_sale_quantity = sales_quantity+quantity
                for srm in for_sale_ranges:
                    if srm.sale_type == COUNT:
                        if not srm.sale_range.title.endswith("+"):
                            if srm.sale_range.end_count is not None:
                                if final_sale_quantity >= srm.sale_range.start_count and final_sale_quantity <= srm.sale_range.end_count:
                                    final_salary = final_salary + (srm.amount * final_sale_quantity)
                            else:
                                if final_sale_quantity == srm.sale_range.start_count:
                                    final_salary = final_salary + (srm.amount * final_sale_quantity)
                        elif srm.sale_range.title.endswith("+"):
                            if final_sale_quantity >= srm.sale_range.start_count:
                                final_salary = final_salary + (srm.amount * final_sale_quantity)

                quantity = final_sale_quantity
                sales_amount = sales_amount + salary_view_next_month_sale_amount
                salary_view_next_month_commission_amount = salary_view_next_month_commission_amount + final_salary
            else:
                salary_view_next_month_commission_amount = salary_view_next_month_commission_amount + final_salary
            send_amount_to_salary_view(user=user, quantity=quantity, sale_amount=sales_amount, commission_amount=salary_view_next_month_commission_amount, amount=final_salary, date=next_month_date)

    if contract.is_holding_contract != True:
        """
        Satış edilən ofisin digər işçilərinin ofisin satışından alacaqları kommissiya
        """
        office_users = user_list().filter(is_superuser=False, is_active=True, office=contract.office)
        other_users = [u for u in office_users if u not in employee_list]
        print(f"{other_users=}")
        for user in other_users:
            try:
                commission = user.commission
            except:
                commission = None
            if commission is not None:
                salary_view_next_month = salary_view_list().filter(employee=user, date=this_month_date).last()
                for_office = commission.for_office * contract.product_quantity
                final_salary = for_office
                send_amount_to_salary_view(user=user, quantity=0, sale_amount=0, commission_amount=final_salary, amount=final_salary, date=next_month_date)

def return_commission_after_cancel_contract(contract):
    """
    Müqavilə düşən statusuna keçdikdə işçilərə verilən komissiyaların geri alınması

    :param contract:
    :return:
    """
    quantity = contract.product_quantity
    sales_amount = contract.product.price * quantity

    now = datetime.date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)

    this_month_date = f"{now.year}-{now.month}-{1}"
    next_month_date = f"{next_m.year}-{next_m.month}-{1}"

    employee_list = list()

    group_leader = contract.group_leader
    manager1 = contract.manager1
    manager2 = contract.manager2
    contract_loan_term = contract.loan_term

    if group_leader is not None:
        employee_list.append(group_leader)
    if manager1 is not None:
        employee_list.append(manager1)
    if manager2 is not None:
        employee_list.append(manager2)

    for user in employee_list:
        try:
            commission = user.commission
        except:
            commission = None

        if commission is not None:
            salary_view_n_m = salary_view_list().filter(employee=user, date= next_month_date).last()
            sales_quantity = salary_view_n_m.sale_quantity
            salary_view_next_month_sale_amount = salary_view_n_m.sales_amount
            new_sales_quantity = sales_quantity-quantity
            new_sales_amount = salary_view_next_month_sale_amount-sales_amount

            cash = commission.cash * contract.product_quantity
            for_team = commission.for_team * contract.product_quantity
            for_office = commission.for_office * contract.product_quantity

            deducted_salary = for_office + for_team # 200

            installments = commission.installment.all()
            
            if contract.payment_style == INSTALLMENT:
                if installments.count() > 0:
                    for inst in installments:
                        if not inst.month_range.title.endswith("+"):
                            if contract_loan_term >= inst.month_range.start_month and contract_loan_term <= inst.month_range.end_month:
                                deducted_salary = deducted_salary + (inst.amount * contract.product_quantity)
                        elif inst.month_range.title.endswith("+"):
                            if int(contract_loan_term) >= inst.month_range.start_month:
                                deducted_salary = deducted_salary + (inst.amount * contract.product_quantity)
            elif contract.payment_style == CASH:
                deducted_salary = deducted_salary + cash
            
            for_sale_ranges = commission.for_sale_range.all()
            sale_a = 0
            final_salary = 0
            if for_sale_ranges.count() > 0:
                for srm in for_sale_ranges:
                    if srm.sale_type == COUNT:
                        if srm.sale_range.end_count is not None:
                            if srm.sale_range.end_count is not None:
                                if sales_quantity >= srm.sale_range.start_count and sales_quantity <= srm.sale_range.end_count:
                                    sale_a = sale_a + (sales_quantity*srm.amount)
                            else:
                                if sales_quantity == srm.sale_range.start_count:
                                    sale_a = sale_a + (sales_quantity*srm.amount)
                        elif srm.sale_range.title.endswith("+"):
                            if sales_quantity >= srm.sale_range.start_count:
                                sale_a = sale_a + (sales_quantity*srm.amount)

                for srm in for_sale_ranges:
                    if srm.sale_type == COUNT:
                        if not srm.sale_range.title.endswith("+"):
                            if srm.sale_range.end_count is not None:
                                if new_sales_quantity >= srm.sale_range.start_count and new_sales_quantity <= srm.sale_range.end_count:
                                    final_salary = final_salary + (srm.amount * new_sales_quantity)
                            else:
                                if new_sales_quantity == srm.sale_range.start_count:
                                    final_salary = final_salary + (srm.amount * new_sales_quantity)
                        elif srm.sale_range.title.endswith("+"):
                            if new_sales_quantity >= srm.sale_range.start_count:
                                final_salary = final_salary + (srm.amount * new_sales_quantity)

                salary_view_n_m.sale_quantity = new_sales_quantity
                salary_view_n_m.sales_amount = new_sales_amount
                salary_view_n_m.commission_amount = salary_view_n_m.commission_amount - sale_a - deducted_salary
                salary_view_n_m.save()

                salary_view_n_m.commission_amount = salary_view_n_m.commission_amount + final_salary
                salary_view_n_m.save()

                salary_view_n_m.final_salary = salary_view_n_m.final_salary - sale_a - deducted_salary
                salary_view_n_m.save()

                salary_view_n_m.final_salary = salary_view_n_m.final_salary + final_salary
                salary_view_n_m.save()
            else:
                salary_view_n_m.sale_quantity = new_sales_quantity
                salary_view_n_m.sales_amount = new_sales_amount
                salary_view_n_m.commission_amount = salary_view_n_m.commission_amount - sale_a - deducted_salary
                salary_view_n_m.save()

                salary_view_n_m.final_salary = salary_view_n_m.final_salary - sale_a - deducted_salary
                salary_view_n_m.save()

                salary_view_n_m.final_salary = salary_view_n_m.final_salary + final_salary
                salary_view_n_m.save()

@delete_emp_activity_history
def salary_operation_delete(instance, func_name=None):
    """
    Bonus, kəsinti, cərimə delete funksiyası
    """
    instance.delete()