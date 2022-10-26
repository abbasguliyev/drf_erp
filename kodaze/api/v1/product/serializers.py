from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.core import DynamicFieldsCategorySerializer

from product.models import (
    Product, 
    Category,
    UnitOfMeasure
)
from company.models import (
    Company,
)
from api.v1.company.serializers import CompanySerializer


class CategorySerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = Category
        fields = "__all__"

class UnitOfMeasureSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = UnitOfMeasure
        fields = "__all__"

class ProductSerializer(DynamicFieldsCategorySerializer):
    company = CompanySerializer(read_only = True, fields=['id', 'name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset = Company.objects.all(), source = "company", write_only= True
    )
    
    category = CategorySerializer(read_only = True, fields=['id', 'category_name'])
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(), source = "category", write_only= True, required=True, allow_null=False
    )

    unit_of_measure = UnitOfMeasureSerializer(read_only = True, fields=['id', 'name'])
    unit_of_measure_id = serializers.PrimaryKeyRelatedField(
        queryset = UnitOfMeasure.objects.all(), source = "unit_of_measure", write_only= True, required=True, allow_null=False
    )
    
    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        product_name = validated_data.get('product_name')
        validated_data['product_name'] = product_name
        company = validated_data['company']
        try:
            product = Product.objects.filter(product_name=product_name, company=company)
            if len(product)>0:
                raise ValidationError
            return super(ProductSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail" : 'Bu ad ilə məhsul artıq əlavə olunub'})
