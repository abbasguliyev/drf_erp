from warehouse.models import WarehouseHistory
from warehouse.api.selectors import warehouse_history_list

def warehouse_history_create(
    *, user,
    company = None,
    sender_warehouse = None,
    receiving_warehouse = None,
    sender_previous_quantity = 0,
    sender_subsequent_quantity = 0,
    recepient_previous_quantity = 0,
    recepient_subsequent_quantity = 0,
    customer = None,
    product = None,
    quantity = None,
    operation_style = None,
    executor = None,
    note = None
) -> WarehouseHistory:
    executor = user
    obj = WarehouseHistory.objects.create(
        company = company,
        sender_warehouse = sender_warehouse,
        receiving_warehouse = receiving_warehouse,
        sender_previous_quantity = sender_previous_quantity,
        sender_subsequent_quantity = sender_subsequent_quantity,
        recepient_previous_quantity = recepient_previous_quantity,
        recepient_subsequent_quantity = recepient_subsequent_quantity,
        customer = customer,
        product = product,
        quantity = quantity,
        operation_style = operation_style,
        executor = executor,
        note = note
    )

    obj.full_clean()
    obj.save()

    return obj