from product.models import UnitOfMeasure, Category, Product
from django.db.models.query import QuerySet

def unit_of_measure_list(*, filters=None) -> QuerySet[UnitOfMeasure]:
    filters = filters or {}
    qs = UnitOfMeasure.objects.all()
    return qs

def category_list(*, filters=None) -> QuerySet[Category]:
    filters = filters or {}
    qs = Category.objects.all()
    return qs

def product_list(*, filters=None) -> QuerySet[Product]:
    filters = filters or {}
    qs = Product.objects.select_related('category', 'unit_of_measure').all()
    return qs
