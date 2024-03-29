from rest_framework.exceptions import ValidationError

from salary.models import (
    MonthRange,
    SaleRange,
    CommissionInstallment,
    CommissionSaleRange, Commission
)
from salary.api.selectors import sale_range_list, month_range_list
from salary.api.decorators import add_amount_to_salary_view_decorator
from django.contrib.auth import get_user_model

User = get_user_model()


def month_range_create(start_month: int, end_month: int = None) -> MonthRange:
    if end_month is not None and end_month > 0:
        if int(start_month) > int(end_month):
            raise ValidationError({'detail': 'Ay aralığını doğru daxil edin'})
        title = f"{start_month}-{end_month}"
    elif end_month is None or end_month == 0:
        if start_month == 0:
            title = f"{start_month}"
        else:
            title = f"{start_month}+"

    # mr = month_range_list().filter(title=title).count()
    # if mr > 0:
    #     raise ValidationError({'detail': 'Bu aralıq artıq daxil edilib'})

    obj = MonthRange.objects.create(title=title, start_month=start_month, end_month=end_month)
    obj.full_clean()
    obj.save()

    return obj

def month_range_update(instance, **data) -> MonthRange:
    start_month = data.get('start_month')
    if start_month is None:
        start_month = instance.start_month
    
    end_month = data.get('end_month')

    if end_month is not None and end_month > 0:
        if int(start_month) > int(end_month):
            raise ValidationError({'detail': 'Ay aralığını doğru daxil edin'})
        title = f"{start_month}-{end_month}"
    elif end_month is None or end_month == 0:
        if start_month == 0:
            title = f"{start_month}"
        else:
            title = f"{start_month}+"

    # mr = month_range_list().filter(title=title).count()
    # if mr > 0:
    #     raise ValidationError({'detail': 'Bu aralıq artıq daxil edilib'})

    instance.title = title
    instance.start_month = start_month
    instance.end_month = end_month
    instance.save()

    return instance

def sale_range_create(start_count: int, end_count: int = None) -> SaleRange:
    if end_count is not None and end_count > 0:
        if int(start_count) > int(end_count):
            raise ValidationError({'detail': 'Satış aralığını doğru daxil edin'})
        title = f"{start_count}-{end_count}"
    elif end_count is None or end_count == 0:
        if start_count == 0:
            title = f"{start_count}"
        else:
            title = f"{start_count}+"

    # mr = sale_range_list().filter(title=title).count()
    # if mr > 0:
    #     raise ValidationError({'detail': 'Bu aralıq artıq daxil edilib'})

    obj = SaleRange.objects.create(title=title, start_count=start_count, end_count=end_count)
    obj.full_clean()
    obj.save()

    return obj

def sale_range_update(instance, **data) -> SaleRange:
    start_count = data.get('start_count')
    if start_count is None:
        start_count = instance.start_count
        
    end_count = data.get('end_count')
    
    if end_count is not None and end_count > 0:
        if int(start_count) > int(end_count):
            raise ValidationError({'detail': 'Satış aralığını doğru daxil edin'})
        title = f"{start_count}-{end_count}"
    elif end_count is None or end_count == 0:
        if start_count == 0:
            title = f"{start_count}"
        else:
            title = f"{start_count}+"

    # mr = sale_range_list().filter(title=title).count()
    # if mr > 0:
    #     raise ValidationError({'detail': 'Bu aralıq artıq daxil edilib'})

    instance.title = title
    instance.start_count = start_count
    instance.end_count = end_count
    instance.save()

    return instance

def commission_installment_create(month_range, amount: float) -> CommissionInstallment:
    obj = CommissionInstallment.object.create(month_range=month_range, amount=amount)
    obj.full_clean()
    obj.save()

    return obj


def commission_sale_range_create(month_range, amount: float, sale_type: str) -> CommissionSaleRange:
    obj = CommissionSaleRange.object.create(month_range=month_range, amount=amount, sale_type=sale_type)
    obj.full_clean()
    obj.save()

    return obj


def commission_create(
        *, commission_name: str,
        for_office: float = 0,
        cash: float = 0,
        for_team: float = 0,
        month_ranges: str = None,
        sale_ranges: str = None,
        creditor_per_cent: int = 0
) -> Commission:
    if for_office is None:
        for_office = 0

    if cash is None:
        cash = 0

    if for_team is None:
        for_team = 0

    if creditor_per_cent is None:
        creditor_per_cent = 0

    commission = Commission.objects.create(
        commission_name=commission_name,
        for_office=for_office,
        cash=cash,
        for_team=for_team,
        creditor_per_cent=creditor_per_cent
    )

    month_ranges_str = month_ranges
    if month_ranges_str is not None:
        month_ranges_list_full = month_ranges_str.split(',')
        month_ranges_list = None
        month_ranges_list = [x for x in month_ranges_list_full if x != ' ' and x!='']
    else:
        month_ranges_list = None

    sale_ranges_str = sale_ranges
    if sale_ranges_str is not None:
        sale_ranges_list_full = sale_ranges_str.split(',')
        sale_ranges_list = None
        sale_ranges_list = [x for x in sale_ranges_list_full if x != ' ' and x!='']
    else:
        sale_ranges_list = None

    if month_ranges_list is not None and len(month_ranges_list) > 0:
        m_list = list()
        for mr_list in month_ranges_list:
            splited_list = mr_list.split('-')
            m_list.append(splited_list)

        ci = CommissionInstallment.objects.bulk_create([
            CommissionInstallment(month_range=MonthRange.objects.get(id=mr[0]), amount=mr[1]) for mr in m_list
        ])
        commission.installment.set(ci)

    if sale_ranges_list is not None and len(sale_ranges_list) > 0:
        s_list = list()
        for sr_list in sale_ranges_list:
            splited_s_list = sr_list.split('-')
            s_list.append(splited_s_list)

        cs = CommissionSaleRange.objects.bulk_create([
            CommissionSaleRange(sale_range=SaleRange.objects.get(id=sr[0]), amount=sr[1], sale_type=sr[2]) for sr in
            s_list
        ])
        commission.for_sale_range.set(cs)

    commission.full_clean()
    commission.save()

    return commission


def commission_update(instance, **data) -> Commission:
    if data.get("month_ranges") is not None:
        month_ranges_str = data.pop("month_ranges")
        if month_ranges_str is not None:
            month_ranges_list_full = month_ranges_str.split(',')
            month_ranges_list = None
            month_ranges_list = [x for x in month_ranges_list_full if x != ' ' and x!='']
        else:
            month_ranges_list = None

        if month_ranges_list is not None and len(month_ranges_list) > 0:
            m_list = list()
            for mr_list in month_ranges_list:
                splited_list = mr_list.split('-')
                m_list.append(splited_list)
            for mr in m_list:
                try:
                    ci = CommissionInstallment.objects.select_related('month_range').get(month_range=MonthRange.objects.get(id=mr[0]), commissions=instance)
                    ci.amount=mr[1]
                    ci.save()
                except:
                    new_ci = CommissionInstallment.objects.create(month_range=MonthRange.objects.get(id=mr[0]), amount=mr[1])
                    new_ci.save()
                    instance.installment.add(new_ci)

    if data.get("sale_ranges") is not None:
        sale_ranges_str = data.pop("sale_ranges")
        if sale_ranges_str is not None:
            sale_ranges_list_full = sale_ranges_str.split(',')
            sale_ranges_list = None
            sale_ranges_list = [x for x in sale_ranges_list_full if x != ' ' and x!='']
        else:
            sale_ranges_list = None

        if sale_ranges_list is not None and len(sale_ranges_list) > 0:
            s_list = list()
            for sr_list in sale_ranges_list:
                splited_s_list = sr_list.split('-')
                s_list.append(splited_s_list)

            for sr in s_list:
                try:
                    cs = CommissionSaleRange.objects.select_related('sale_range').get(sale_range=SaleRange.objects.get(id=sr[0]), commissions=instance)
                    cs.amount = sr[1]
                    cs.sale_type = sr[2]
                    cs.save()
                except:
                    new_cs = CommissionSaleRange.objects.create(sale_range=SaleRange.objects.get(id=sr[0]), amount=sr[1], sale_type=sr[2])
                    new_cs.save()
                    instance.for_sale_range.add(new_cs)
    obj = Commission.objects.filter(id=instance.id).update(**data)
    return obj

@add_amount_to_salary_view_decorator
def creditor_permission_add_to_salary_view(employee, amount, date, salary_date=None, func_name="creditor_permission"):
    pass