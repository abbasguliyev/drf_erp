from rest_framework.exceptions import ValidationError
from product.api.selectors import product_list
from warehouse.api.selectors import stock_list, warehouse_list, holding_warehouse_list
from warehouse.api.services import warehouse_service, stock_service, warehouse_history_service
from warehouse import TRANSFER

def holding_office_product_transfer_service(*, user, products_and_quantity: str, company, warehouse, note:str=None):
    if warehouse.company != company:
        raise ValidationError({'detail': 'Anbar qeyd edilmiş şirkətə aid deyil'})

    warehouse = warehouse_list().filter(office=warehouse).last()
    if warehouse is None:
        raise ValidationError({'detail': 'Ofis anbarı tapılmadı'})

    products_and_quantity_list_full = products_and_quantity.split(',')
    products_and_quantity_list = None
    products_and_quantity_list = [
        x for x in products_and_quantity_list_full if x != ' ' and x != '']

    for product_and_quantity in products_and_quantity_list:
        new_list = product_and_quantity.split('-')
        product_id = new_list[0]
        quantity = int(new_list[1])

        holding_warehouse = holding_warehouse_list().filter(id=product_id).last()
        product = holding_warehouse.product
        sender_previous_quantity = holding_warehouse.quantity

        if quantity > holding_warehouse.useful_product_count:
            continue

        if holding_warehouse.quantity == 0:
            continue

        stock = stock_list().filter(warehouse=warehouse, product=product).last()

        if stock is None:
            recepient_previous_quantity = 0
            stock_service.stock_create(
                warehouse=warehouse,
                product=product,
                quantity=quantity,
                useful_product_count=quantity,
                note=None
            )
            stock = stock_list().filter(warehouse=warehouse, product=product).last()
        else:
            recepient_previous_quantity = stock.quantity
            stock_service.add_product_to_stock(stock=stock, product_quantity=quantity)

        recepient_subsequent_quantity = stock.quantity

        holding_warehouse.quantity = holding_warehouse.quantity - quantity
        holding_warehouse.useful_product_count = holding_warehouse.useful_product_count - quantity
        holding_warehouse.save()
        sender_subsequent_quantity = holding_warehouse.quantity

        warehouse_history_service.warehouse_history_create(
            user = user, sender_warehouse="Holding anbarı", 
            receiving_warehouse= f"{warehouse.name}", 
            sender_previous_quantity=sender_previous_quantity, sender_subsequent_quantity=sender_subsequent_quantity,
            recepient_previous_quantity=recepient_previous_quantity, recepient_subsequent_quantity=recepient_subsequent_quantity,
            product=product.product_name, quantity = quantity, operation_style=TRANSFER, executor=user, note=note
        )


def between_office_product_transfer_service(*, user, products_and_quantity: str, company, sender_office, recipient_office, note: str = None):
    if sender_office.company != company:
        raise ValidationError(
            {'detail': 'Göndərən Anbar qeyd edilmiş şirkətə aid deyil'})

    if recipient_office.company != company:
        raise ValidationError(
            {'detail': 'Qəbul edən Anbar qeyd edilmiş şirkətə aid deyil'})

    products_and_quantity_list_full = products_and_quantity.split(',')
    products_and_quantity_list = None
    products_and_quantity_list = [x for x in products_and_quantity_list_full if x != ' ' and x != '']

    sender_warehouse = warehouse_list().filter(office=sender_office).last()
    recipient_warehouse = warehouse_list().filter(office=recipient_office).last()

    for product_and_quantity in products_and_quantity_list:
        new_list = product_and_quantity.split('-')
        product_id = new_list[0]
        quantity = int(new_list[1])

        product = product_list().filter(pk=product_id).last()

        sender_stock = stock_list().filter(warehouse=sender_warehouse, product=product).last()
        recipient_stock = stock_list().filter(warehouse=recipient_warehouse, product=product).last()
        
        sender_previous_quantity = sender_stock.quantity

        if quantity > sender_stock.useful_product_count:
            continue

        stock_service.reduce_product_from_stock(stock=sender_stock, product_quantity=quantity)
        
        sender_subsequent_quantity = sender_stock.quantity

        if recipient_stock is None:
            recepient_previous_quantity = 0
            stock_service.stock_create(
                warehouse=recipient_warehouse,
                product=product,
                quantity=quantity,
                useful_product_count=quantity,
                note=None
            )
            recipient_stock = stock_list().filter(warehouse=recipient_warehouse, product=product).last()
        else:
            recepient_previous_quantity = recipient_stock.quantity

            stock_service.add_product_to_stock(stock=recipient_stock, product_quantity=quantity)
        
        recepient_subsequent_quantity = recipient_stock.quantity
    
        warehouse_history_service.warehouse_history_create(
            user = user, sender_warehouse=f"{sender_warehouse.name}",
            receiving_warehouse= f"{recipient_warehouse.name}", 
            sender_previous_quantity=sender_previous_quantity, sender_subsequent_quantity=sender_subsequent_quantity,
            recepient_previous_quantity=recepient_previous_quantity, recepient_subsequent_quantity=recepient_subsequent_quantity,
            product=product.product_name, quantity = quantity, operation_style=TRANSFER, executor=user, note=note
        )

def office_to_holding_product_transfer(*, user, products_and_quantity: str, company, warehouse):
    if warehouse.company != company:
        raise ValidationError(
            {'detail': 'Anbar qeyd edilmiş şirkətə aid deyil'})

    warehouse = warehouse_list().filter(office=warehouse).last()
    if warehouse is None:
        raise ValidationError({'detail': 'Ofis anbarı tapılmadı'})

    products_and_quantity_list_full = products_and_quantity.split(',')
    products_and_quantity_list = None
    products_and_quantity_list = [x for x in products_and_quantity_list_full if x != ' ' and x != '']

    for product_and_quantity in products_and_quantity_list:
        new_list = product_and_quantity.split('-')
        product_id = new_list[0]
        quantity = int(new_list[1])

        product = product_list().filter(pk=product_id).last()
        sender_stock = stock_list().filter(warehouse=warehouse, product=product).last()

        sender_previous_quantity = sender_stock.quantity

        if quantity > sender_stock.useful_product_count:
            continue

        stock_service.reduce_product_from_stock(stock=sender_stock, product_quantity=quantity)
        sender_subsequent_quantity = sender_stock.quantity

        holding_warehouse = holding_warehouse_list().filter(product__id=product_id).last()

        if holding_warehouse is None:
            recepient_previous_quantity = 0
            warehouse_service.holding_warehouse_create(
                product=product,
                quantity=quantity,
                useful_product_count=quantity,
                unuseful_product_count=0
            )
            holding_warehouse = holding_warehouse_list().filter(product__id=product_id).last()
        else:
            recepient_previous_quantity = holding_warehouse.quantity

            holding_warehouse.quantity = holding_warehouse.quantity + quantity
            holding_warehouse.useful_product_count = holding_warehouse.useful_product_count + quantity
            holding_warehouse.save()
        
        recepient_subsequent_quantity = holding_warehouse.quantity

        warehouse_history_service.warehouse_history_create(
            user = user, sender_warehouse=f"{warehouse.name}",
            receiving_warehouse= "Holding anbarı", 
            sender_previous_quantity=sender_previous_quantity, sender_subsequent_quantity=sender_subsequent_quantity,
            recepient_previous_quantity=recepient_previous_quantity, recepient_subsequent_quantity=recepient_subsequent_quantity,
            product=product.product_name, quantity = quantity, operation_style=TRANSFER, executor=user
        )
