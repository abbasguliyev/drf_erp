from rest_framework.exceptions import ValidationError
from contract.models import ContractGift
from product.api.selectors import product_list
from warehouse.api.selectors import holding_warehouse_list, warehouse_list, stock_list
from warehouse.api.services import warehouse_history_service, stock_service
from warehouse import SATIS, HEDIYYE
from cashbox.api.decorators import cashbox_operation_decorator


@cashbox_operation_decorator
def contract_gift_cashbox(*, user=None, employee, office, company, date, note, amount, customer, func_name="contract_gift"):
    pass

def contract_gift_create(
    *, user=None,
    products,
    quantities,
    contract
) -> ContractGift:
    company = contract.company
    office = contract.office
    product_quantity_list = quantities.split(',')

    for i, prod in enumerate(products):
        product = product_list().filter(pk=prod.id).last()
        # total_price += (float(product.price)*quantities[i])
        if contract.is_holding_contract == True:
            stock = holding_warehouse_list().filter(product=product).last()
            if stock is None:
                raise ValidationError({'detail': 'Xəta baş verdi. Məhsulların stokda olub olmadığın dəqiqləşdirin.'})
            else:
                if stock.quantity < int(product_quantity_list[i]):
                    raise ValidationError({'detail': 'Xəta baş verdi. Məhsulların stokda yetəri qədər olub olmadığın dəqiqləşdirin.'})
        else:
            warehouse = warehouse_list().filter(company=company, office=office).last()
            stock = stock_list().filter(warehouse=warehouse, product=product).last()
            if stock is None or stock.quantity == 0:
                raise ValidationError({'detail': 'Xəta baş verdi. Məhsullarının stokda olub olmadığın dəqiqləşdirin.'})
            else:
                if stock.quantity < int(product_quantity_list[i]):
                    raise ValidationError({'detail': 'Xəta baş verdi. Məhsullarının stokda yetəri qədər olub olmadığın dəqiqləşdirin.'})
    for i, product in enumerate(products):
        if contract.is_holding_contract == True:
            stock = holding_warehouse_list().filter(product=product).last()
            stock_previous_quantity = stock.quantity
            stock.quantity = stock.quantity - int(product_quantity_list[i])
            stock.useful_product_count = stock.useful_product_count - int(product_quantity_list[i])
            stock.save()
            stock_subsequent_quantity = stock.quantity
            warehouse_history_service.warehouse_history_create(
                user = user, sender_warehouse="Holding anbarı", 
                sender_previous_quantity=stock_previous_quantity, sender_subsequent_quantity=stock_subsequent_quantity, 
                customer=contract.customer, product=product.product_name, quantity = int(product_quantity_list[i]), 
                operation_style=HEDIYYE, executor=user, note=None
            )
        else:
            warehouse = warehouse_list().filter(company=company, office=office).last()
            stock = stock_list().filter(warehouse=warehouse, product=product).last()
            stock_previous_quantity = stock.quantity
            stock_service.reduce_product_from_stock(stock=stock, product_quantity=int(product_quantity_list[i]))
            stock_subsequent_quantity = stock.quantity
            warehouse_history_service.warehouse_history_create(
                user = user, sender_warehouse="Holding anbarı", 
                sender_previous_quantity=stock_previous_quantity, sender_subsequent_quantity=stock_subsequent_quantity, 
                customer=contract.customer, product=product.product_name, quantity = int(product_quantity_list[i]), 
                operation_style=HEDIYYE, executor=user, note=None
            )
        
        if product.price > 0:
            contract_gift_cashbox(
                user=user, employee=contract.group_leader, office=office, company=company, 
                date=contract.contract_date, note=f"{product.product_name} hədiyyəsinə görə ödədi.", amount=(product.price*int(product_quantity_list[i])), 
                customer=contract.customer, func_name="contract_gift"
            )
        
        obj = ContractGift.objects.create(product=product, contract=contract, quantity=int(product_quantity_list[i]))
        obj.full_clean()
        obj.save()