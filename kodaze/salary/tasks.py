from celery import shared_task

from api.v1.salary.utils import give_commission_after_contract


@shared_task(name='create_prim_task')
def create_prim_task(id):
    give_commission_after_contract(contract_id=id)
