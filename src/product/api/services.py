from product.models import UnitOfMeasure, Category, Product
from product.api.selectors import product_list

def unit_of_measure_create(*, name: str) -> UnitOfMeasure:
    obj = UnitOfMeasure.objects.create(name=name)
    obj.full_clean()
    obj.save()

    return obj


def category_create(*, category_name: str) -> Category:
    obj = Category.objects.create(category_name=category_name)
    obj.full_clean()
    obj.save()

    return obj

def product_create(
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
) -> Product:
    obj = Product.objects.create(
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
    obj.full_clean()
    obj.save()

    return obj

def procut_update(instance, **data) -> Product:
    obj = product_list().filter(pk=instance.id).update(**data)
    return obj

def product_delete(instance):
    instance.delete()

def calculate_products_total_price(product_ids, quantities) -> str:
    total_price = 0
    for i, product_id in enumerate(product_ids):
        product = product_list().filter(pk=product_id).last()
        total_price += (float(product.price)*quantities[i])
    return f"{total_price}"