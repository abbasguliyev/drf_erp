from rest_framework.exceptions import ValidationError
from product.api.selectors import product_list
from warehouse.api.selectors import stock_list, warehouse_list
from warehouse.api.services import warehouse_service, stock_service

def holding_office_product_transfer_service(*, products_and_quantity: str, company, warehouse):
    if warehouse.company != company:
        raise ValidationError({'detail': 'Anbar qeyd edilmiş şirkətə aid deyil'})
    
    warehouse = warehouse_list().filter(office=warehouse).last()
    if warehouse is None:
        raise ValidationError({'detail': 'Ofis anbarı tapılmadı'})

    products_and_quantity_list = products_and_quantity.split(',')
    for product_and_quantity in products_and_quantity_list:
        new_list = product_and_quantity.split('-')
        product_id = new_list[0]
        quantity = int(new_list[1])

        product = product_list().filter(pk=product_id).last()
        if quantity > product.quantity:
            continue
        
        if product.quantity == 0:
            continue

        stock = stock_list().filter(warehouse=warehouse, product=product).last()

        if stock is None:
            stock_service.stock_create(
                warehouse=warehouse, 
                product=product, 
                quantity=quantity, 
                useful_product_count=quantity,
                note=None
            )
        else:
            stock_service.add_product_to_stock(stock=stock, product_quantity=quantity)

        product.quantity = product.quantity - quantity
        product.useful_product_count = product.useful_product_count - quantity
        product.save()
        

def between_office_product_transfer_service(*, products_and_quantity: str, company, sender_office, recipient_office):
    products_and_quantity_list = products_and_quantity.split(',')
    sender_warehouse = warehouse_list().filter(office=sender_office).last()
    recipient_warehouse = warehouse_list().filter(office=recipient_office).last()

    for product_and_quantity in products_and_quantity_list:
        new_list = product_and_quantity.split('-')
        product_id = new_list[0]
        quantity = int(new_list[1])

        product = product_list().filter(pk=product_id).last()
        
        sender_stock = stock_list().filter(warehouse=sender_warehouse, product=product)
        recipient_stock = stock_list().filter(warehouse=recipient_warehouse, product=product)

        if quantity > product.quantity:
            continue
        