from warehouse.models import Stock
from rest_framework.exceptions import ValidationError
import datetime

def stock_create(
    *, 
    warehouse, 
    product, 
    quantity: int = 0,
    useful_product_count: int = 0,
    changed_product_count: int = 0,
    note: str = None
) -> Stock:
    useful_product_count = quantity
    obj = Stock.objects.create(
        warehouse=warehouse, 
        product=product, 
        quantity=quantity, 
        useful_product_count=useful_product_count, 
        changed_product_count=changed_product_count, 
        note=note
    )
    obj.full_clean()
    obj.save()

    return obj

def reduce_product_from_stock(stock: Stock, product_quantity: int) -> int:
    stock.quantity = stock.quantity - product_quantity
    if stock.useful_product_count == 0:
        raise ValidationError({'detail': 'Stokda yetəri qədər məhsul yoxdur'})
    if stock.useful_product_count < product_quantity:
        raise ValidationError({'detail': 'Stokda yetəri qədər məhsul yoxdur'})
    stock.useful_product_count = stock.useful_product_count - product_quantity
    stock.save()
    if stock.quantity == 0:
        stock.delete()
    return stock.quantity


def add_product_to_stock(stock: Stock, product_quantity: int) -> int:
    stock.quantity = stock.quantity + product_quantity
    stock.useful_product_count = stock.useful_product_count + product_quantity
    stock.save()
    return stock.quantity