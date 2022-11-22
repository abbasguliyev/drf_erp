from celery import shared_task

from salary.api.utils import give_commission_after_contract


@shared_task(name='create_commission_task')
def create_commission_task(id):
    give_commission_after_contract(contract_id=id)
