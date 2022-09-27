from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from product.models import (
    Product, 
)
from company.models import (
    Company,
)
from restAPI.v1.company.serializers import CompanySerializer


class ProductSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only = True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset = Company.objects.all(), source = "company", write_only= True
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
            raise ValidationError({"detail" : 'Bu name ilə məhsul artıq əlavə olunub'})
