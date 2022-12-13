from warehouse.models import WarehouseRequest
from warehouse import WAITING
from warehouse.api.selectors import holding_warehouse_list, warehouse_list
from rest_framework.exceptions import ValidationError

def warehouse_request_create(
    *, user,
    employee_who_sent_the_request = None,
    product_and_quantity,
    note: str = None,
    warehouse = None,
    status = WAITING,
    execution_date = None
) -> WarehouseRequest:
    products_and_quantity_list_full = product_and_quantity.split(',')
    products_and_quantity_list = None
    products_and_quantity_list = [
        x for x in products_and_quantity_list_full if x != ' ' and x != '']

    for product_and_quantity in products_and_quantity_list:
        new_list = product_and_quantity.split('-')
        product_id = new_list[0]
        quantity = int(new_list[1])

        holding_warehouse = holding_warehouse_list().filter(pk=product_id)
        if holding_warehouse.count() == 0:
            raise ValidationError({'detail': 'Sorğu üçün göndərilən məhsulların holding anbarında olması lazımdır'})
        if quantity > holding_warehouse.last().useful_product_count:
            raise ValidationError({'detail': 'Sorğu üçün göndərilən məhsulların sayı holding anbarındakı saya uyğun olmalıdır'})

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