from celery import shared_task
from account.api.selectors import user_list
from salary.api.utils import give_commission_after_contract
from salary.api.services import salary_pay_service
from salary.api.selectors import salary_view_list

@shared_task(name='create_commission_task')
def create_commission_task(id):
    give_commission_after_contract(contract_id=id)

@shared_task(name='salary_pay_task')
def salary_pay_task(executor_id, salary_views):
    executor = user_list().filter(pk=executor_id).last()
    for salary_view in salary_views:
        sw = salary_view_list().filter(pk=salary_view).last()
        salary_pay_service.salary_pay_create(executor=executor, salary_view=sw, func_name='salary_pay_create')

