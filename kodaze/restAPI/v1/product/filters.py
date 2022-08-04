import django_filters

from product.models import (
    Mehsullar,
)

class MehsullarFilter(django_filters.FilterSet):
    class Meta:
        model = Mehsullar
        fields = {
            'mehsulun_adi': ['exact', 'icontains'],
            'qiymet': ['exact', 'gte', 'lte'],
            'shirket__shirket_adi': ['exact', 'icontains'],
            'is_hediyye': ['exact'],
        }
