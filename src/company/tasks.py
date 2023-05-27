from celery import shared_task
from account.api.selectors import user_list


@shared_task(bind = True)
def deactive_employees_of_a_specific_company(self, company_id):
    employees = user_list().filter(company_id = company_id)
    
    for i in employees:
        i.is_active = False
        i.save()
    
    return 'Done!'