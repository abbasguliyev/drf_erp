from warehouse.models import ChangeUnuselessOperation
from warehouse.api.selectors import holding_warehouse_list

def change_unuseless_operation_create(*, products_and_quantity: str, note: str = "") -> ChangeUnuselessOperation:
    products_and_quantity_list = products_and_quantity.split(',')
    for product_and_quantity in products_and_quantity_list:
        new_list = product_and_quantity.split('-')
        product_id = new_list[0]
        quantity = int(new_list[1])

        holding_warehouse_product = holding_warehouse_list().filter(pk=product_id).last()

        if quantity > holding_warehouse_product.quantity:
            continue

        holding_warehouse_product.quantity = holding_warehouse_product.quantity - quantity
        holding_warehouse_product.useful_product_count -= quantity
        holding_warehouse_product.unuseful_product_count += quantity
        
        holding_warehouse_product.save()
    
    obj = ChangeUnuselessOperation.objects.create(products_and_quantity=products_and_quantity_list, note=note)
    obj.full_clean()
    obj.save()

    return obj
    
    

