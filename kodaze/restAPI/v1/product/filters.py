import django_filters

from product.models import (
    Product,
)

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'product_name': ['exact', 'icontains'],
            'price': ['exact', 'gte', 'lte'],
            'company__name': ['exact', 'icontains'],
            'is_hediyye': ['exact'],
        }
