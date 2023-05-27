import datetime
from warehouse.models import WarehouseRequest
from warehouse import WAITING, DONE, REJECT
from warehouse.api.selectors import holding_warehouse_list, warehouse_list, warehouse_request_list
from rest_framework.exceptions import ValidationError
from warehouse.api.services.product_transfer_service import holding_office_product_transfer_service

def warehouse_request_create(
    *, user,
    employee_who_sent_the_request = None,
    product_and_quantity,
    note: str = None,
    warehouse = None,
    status = WAITING,
    execution_date = None
) -> WarehouseRequest:
    employee_who_sent_the_request = user
    office = employee_who_sent_the_request.office
    warehouse = warehouse_list().filter(office=office).last()

    obj = WarehouseRequest.objects.create(
        employee_who_sent_the_request=employee_who_sent_the_request, 
        product_and_quantity=product_and_quantity,
        note=note,
        warehouse=warehouse,
        status=status,
        execution_date=execution_date
    )
    obj.full_clean()
    obj.save()

    return obj

def warehouse_request_execute(*, instance_id, user, products_and_quantity=None, company=None, office=None, note=None, status):
    obj = warehouse_request_list().filter(pk=instance_id).last()
    execution_date = datetime.date.today()

    if obj.status == WAITING:
        if status == REJECT:
            obj.status = REJECT
            obj.note = note
            obj.execution_date = execution_date
            obj.save()
        elif status == DONE:
            if products_and_quantity is None or company is None or office is None:
                raise ValidationError({'detail': 'Məlumatları doğru daxil edin'})

            holding_office_product_transfer_service(
                user=user, products_and_quantity=products_and_quantity,
                company=company, warehouse=office, note=note
            )
            obj.status = DONE
            obj.note = note
            obj.execution_date = execution_date
            obj.save()
        else:
            raise ValidationError({'detail': 'Məlumatları doğru daxil edin'})
    else:
        raise ValidationError({'detail': 'Ancaq yerinə yetirilməmiş sorğuları icra etmək mümkündür.'})