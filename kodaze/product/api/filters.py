import django_filters

from product.models import (
    Product,
    Category,
    UnitOfMeasure
)


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'product_name': ['exact', 'icontains'],
            'purchase_price': ['exact', 'gte', 'lte'],
            'price': ['exact', 'gte', 'lte'],
            'barcode': ['exact', 'icontains'],
            'is_gift': ['exact'],
        }


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'category_name': ['exact', 'icontains']
        }


class UnitOfMeasureFilter(django_filters.FilterSet):
    class Meta:
        model = UnitOfMeasure
        fields = {
            'name': ['exact', 'icontains']
        }
