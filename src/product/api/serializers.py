from rest_framework import serializers
from core.utils.base_serializer import DynamicFieldsCategorySerializer

from product.models import (
    Product,
    Category,
    UnitOfMeasure
)

from product.api.selectors import unit_of_measure_list, category_list


class CategorySerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = Category
        fields = "__all__"


class UnitOfMeasureSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = UnitOfMeasure
        fields = "__all__"


class ProductSerializer(DynamicFieldsCategorySerializer):
    category = CategorySerializer(read_only=True, fields=['id', 'category_name'])
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=category_list(), source="category", write_only=True, required=True, allow_null=False
    )

    unit_of_measure = UnitOfMeasureSerializer(read_only=True, fields=['id', 'name'])
    unit_of_measure_id = serializers.PrimaryKeyRelatedField(
        queryset=unit_of_measure_list(), source="unit_of_measure", write_only=True, required=True, allow_null=False
    )

    class Meta:
        model = Product
        fields = "__all__"
