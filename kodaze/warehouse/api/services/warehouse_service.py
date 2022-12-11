from warehouse.models import Warehouse, HoldingWarehouse
from warehouse.api.selectors import warehouse_list
from product.api.selectors import product_list
from product.api.services import product_create

def warehouse_create(
    *, name: str, 
    office,
    company = None
) -> Warehouse:
    obj = Warehouse.objects.create(name=name, office=office, company=office.company)
    obj.full_clean()
    obj.save()

    return obj

def warehouse_update(instance, data) -> Warehouse:
    obj = warehouse_list().filter(pk=instance.id).update(**data)
    obj.save()

    return obj

def warehouse_delete(instance):
    instance.is_active = False
    instance.save()

def holding_warehouse_create(
    *, product, quantity: int = 0, 
    useful_product_count: int = 0, 
    unuseful_product_count: int = 0
) -> HoldingWarehouse:
    useful_product_count = quantity
    obj = HoldingWarehouse.objects.create(
        product=product, 
        quantity=quantity,
        useful_product_count=useful_product_count, 
        unuseful_product_count=unuseful_product_count
    )
    obj.full_clean()
    obj.save()

    return obj

def product_add_to_holding_warehouse(
    *, product_name: str,
    barcode = None,
    category = None,
    unit_of_measure = None,
    purchase_price = 0,
    price = 0,
    guarantee: int = 0,
    is_gift: bool = False,
    weight: float = None,
    width: float = None,
    length: float = None,
    height: float = None,
    volume: float = None,
    note: str = None,
    product_image = None,
    quantity: int = 0,
    useful_product_count: int = 0,
    unuseful_product_count: int = 0
):
    product_search = product_list().filter(product_name=product_name, barcode=barcode)
    if product_search.count() > 0:
        product = product_search.last()
        product.product_name = product_name
        product.barcode = barcode
        product.category = category
        product.unit_of_measure = unit_of_measure
        product.purchase_price = purchase_price
        product.price = price
        product.guarantee = guarantee
        product.is_gift = is_gift
        product.weight = weight
        product.width = width
        product.length = length
        product.height = height
        product.volume = volume
        product.note = note
        product.product_image = product_image

        product.save()
    else:
        product = product_create(
            product_name = product_name,
            barcode = barcode,
            category = category,
            unit_of_measure = unit_of_measure,
            purchase_price = purchase_price,
            price = price,
            guarantee = guarantee,
            is_gift = is_gift,
            weight = weight,
            width = width,
            length = length,
            height = height,
            volume = volume,
            note = note,
            product_image = product_image
        )
        product.full_clean()
        product.save()
    
    useful_product_count = quantity

    holding_warehouse = holding_warehouse_create(
        product=product, 
        quantity=quantity,
        useful_product_count=useful_product_count,
        unuseful_product_count=unuseful_product_count
    )

    holding_warehouse.save()