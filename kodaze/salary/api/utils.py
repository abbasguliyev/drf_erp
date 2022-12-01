import datetime

from contract import INSTALLMENT, CASH
from contract.models import Contract
from salary import COUNT, FIX
from salary.models import (
    SalaryView,
    GivenCommissionAfterSignContract
)
import pandas as pd
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from salary.api.selectors import salary_view_list
from salary.api.decorators import delete_emp_activity_history
from account.api.selectors import user_list

User = get_user_model()


def give_commission_after_contract(
        contract_id: int
):
    """
    Müqavilə imzalanarkən işçiyə təyin olunmuş komissiya üsuluna görə təyin olunmuş məbləğlərin verilməsi

    :param contract_id:
    :return:
    """
    contract = Contract.objects.get(id=contract_id)
    quantity = contract.product_quantity
    sales_amount = float(contract.product.price) * float(quantity)

    now = datetime.date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)

    this_month_date = f"{now.year}-{now.month}-{1}"
    next_month_date = f"{next_m.year}-{next_m.month}-{1}"

    user_list = list()

    group_leader = contract.group_leader
    manager1 = contract.manager1
    manager2 = contract.manager2

    user_list.append(group_leader)
    user_list.append(manager1)
    user_list.append(manager2)

    for user in user_list:
        commission = user.commission
        if commission is not None:
            salary_view_this_month = salary_view_list().filter(employee=user, date=this_month_date).last()

            cash = commission.cash * contract.product_quantity
            for_office = commission.for_office * contract.product_quantity
            for_team = commission.for_office * contract.product_quantity
            creditor_per_cent = commission.creditor_per_cent * contract.product_quantity

            installments = commission.installment.all()
            for_sale_ranges = commission.for_sale_range.all()

            final_salary = for_office + for_team + creditor_per_cent
            commission_amount = 0

            contract_loan_term = contract.loan_term
            contract_payment_style = contract.payment_style

            if contract_payment_style == INSTALLMENT:
                if installments.count() > 0:
                    for inst in installments.all():
                        if not inst.month_range.title.endswith("+"):
                            if int(contract_loan_term) >= inst.month_range.start_month and int(
                                    contract_loan_term) <= inst.month_range.end_month:
                                final_salary = final_salary + (inst.amount * contract.product_quantity)
                                commission_amount = inst.amount * contract.product_quantity
                        elif inst.month_range.title.endswith("+"):
                            if int(contract_loan_term) >= inst.month_range.start_month:
                                final_salary = final_salary + (inst.amount * contract.product_quantity)
                                commission_amount = inst.amount * contract.product_quantity
            elif contract_payment_style == CASH:
                final_salary = final_salary + cash

            if for_sale_ranges.count() > 0:
                sales_quantity = salary_view_this_month.sales_quantity

                for srm in for_sale_ranges:
                    if srm.sale_type == COUNT:
                        if not srm.sale_range.title.endswith("+"):
                            if int(sales_quantity) >= srm.sale_range.start_count and int(
                                    sales_quantity) <= srm.sale_range.end_count:
                                final_salary = final_salary + (srm.amount * contract.product_quantity)
                                commission_amount = srm.amount * contract.product_quantity
                        elif srm.sale_range.title.endswith("+"):
                            if int(sales_quantity) >= srm.sale_range.start_count:
                                final_salary = final_salary + (srm.amount * contract.product_quantity)
                                commission_amount = srm.amount * contract.product_quantity

            given_commission_after_sign_contract_create(user=user, contract=contract, amount=final_salary)

            send_sale_quantity_to_salary_view(user=user, quantity=quantity, amount=sales_amount, date=this_month_date)
            send_amount_to_salary_view(user=user, amount=final_salary, commission_amount=commission_amount, date=next_month_date)


def send_amount_to_salary_view(user: User, amount: float, date) -> SalaryView:
    """
    İşçi ə/h cədvəlində yekun məbləğə verilmiş məbləğin əlavə edilməsi
    """
    salary_view = salary_view_list().filter(employee=user, date= date).last()
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
    salary_view.sales_quantity = salary_view.sale_quantity + quantity
    salary_view.sales_amount = salary_view.sales_amount + amount
    salary_view.commission_amount = commission_amount
    salary_view.save()

    return salary_view

def get_back_sale_quantity_from_salary_view(user: User, quantity: float, amount: float, date) -> SalaryView:
    """
    İşçi ə/h cədvəlində satış sayından verilmiş miqdarın çıxılması
    """
    salary_view = salary_view_list().filter(employee=user, date= date).last()
    salary_view.sales_quantity = salary_view.sale_quantity - quantity
    salary_view.sales_amount = salary_view.sales_amount - amount
    salary_view.save()

    return salary_view


def create_fix_commission():
    """
    İşçilərə fix komissiyaların verilməsi
    """
    users = user_list().filter(is_active=True)
    now = datetime.date.today()
    this_month = f"{now.year}-{now.month}-{1}"

    sale_range_final_salary = 0

    for user in users:
        salary_view_this_month = salary_view_list().filter(employee=user, date=this_month).last()
        if user.commission is not None:
            for_sale_ranges = user.commission.for_sale_range
            if for_sale_ranges.count() > 0:
                sales_quantity = salary_view_this_month.sales_quantity

                for srm in for_sale_ranges:
                    if srm.sale_type == FIX:
                        if not srm.sale_range.title.endswith("+"):
                            if int(sales_quantity) >= srm.sale_range.start_count and int(
                                    sales_quantity) <= srm.sale_range.end_count:
                                sale_range_final_salary += srm.amount
                        elif srm.sale_range.title.endswith("+"):
                            if int(sales_quantity) >= srm.sale_range.start_count:
                                sale_range_final_salary += srm.amount

            salary_view_this_month.final_salary = salary_view_this_month.final_salary + sale_range_final_salary + float(user.commission.cash)
            salary_view_this_month.save()


def given_commission_after_sign_contract_create(
        user: User,
        contract: Contract,
        amount: float
) -> GivenCommissionAfterSignContract:
    """
    Müqavilə imzalanarkən işçiyə verilən komissiyaların database-də toplaması üçün funksiya.
    Databse-də toplamaq səbəbi müqavilə düşən statusuna keçdikdə işçilərə verilən komissiyaların
    qaytarılmasını rahatlaşdırmaqdır

    :param user:
    :param contract:
    :param amount:
    :return:
    """
    obj = GivenCommissionAfterSignContract.objects.create(user=user, contract=contract, amount=amount)
    obj.save()
    return obj


def return_commission_after_cancel_contract(contract):
    """
    Müqavilə düşən statusuna keçdikdə işçilərə verilən komissiyaların geri alınması

    :param contract:
    :return:
    """
    quantity = contract.product_quantity
    sales_amount = float(contract.product.price) * float(quantity)

    now = datetime.date.today()
    d = pd.to_datetime(f"{now.year}-{now.month}-{1}")
    next_m = d + pd.offsets.MonthBegin(1)

    this_month_date = f"{now.year}-{now.month}-{1}"
    next_month_date = f"{next_m.year}-{next_m.month}-{1}"

    given_commissions = GivenCommissionAfterSignContract.objects.filter(contract=contract)

    for gc in given_commissions:
        user = gc.user
        amount = gc.amount

        get_back_sale_quantity_from_salary_view(user=user, quantity=quantity, amount=sales_amount, date=this_month_date)
        get_back_amount_from_salary_view(user=user, amount=amount, date=next_month_date)

@delete_emp_activity_history
def salary_operation_delete(instance, func_name=None):
    """
    Avans, bonus, kəsinti, cərimə delete funksiyası
    """
    # if instance.is_paid == True:
    #     raise ValidationError({"detail": "Ödənilmiş məbləği silə bilmərsiniz"})
    instance.delete()