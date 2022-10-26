from rest_framework import serializers
from api.core import DynamicFieldsCategorySerializer

from rest_framework.exceptions import ValidationError

from warehouse.models import (
    Operation, 
    Warehouse, 
    WarehouseRequest, 
    Stock,
)
from product.models import (
    Product, 
)

from account.models import (
    User, 
)

from company.models import (
    Company,
    Office,
)

from api.v1.account.serializers import UserSerializer
from api.v1.product.serializers import ProductSerializer

from api.v1.company.serializers import OfficeSerializer, CompanySerializer

class WarehouseSerializer(DynamicFieldsCategorySerializer):
    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    office = OfficeSerializer(read_only=True, fields=['id', 'name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.select_related('company').all(), source='office', write_only=True
    )

    class Meta:
        model = Warehouse
        fields = "__all__"

    def create(self, validated_data):
        name = validated_data.get('name')
        validated_data['name'] = name.upper()
        try:
            return super(WarehouseSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail" : 'Bu ad ilə warehouse artıq əlavə olunub'})

class OperationSerializer(DynamicFieldsCategorySerializer):
    executor = UserSerializer(read_only=True, fields = ['id', 'fullname'])
    shipping_warehouse = WarehouseSerializer(read_only=True, fields = ['id', 'name'])
    receiving_warehouse = WarehouseSerializer(read_only=True, fields = ['id', 'name'])

    shipping_warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.select_related('office', 'company').all(), source="shipping_warehouse", write_only=True, required= True
    )
    receiving_warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.select_related('office', 'company').all(), source="receiving_warehouse", write_only=True, required= True
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        product_and_quantity = instance.product_and_quantity
        operation_type = instance.operation_type
        stok_ile_gelen_quantity = instance.quantity
        data = dict()
        if(product_and_quantity is not None):
            if operation_type == "transfer":
                product_and_quantity_list = product_and_quantity.split(",")
                for m in product_and_quantity_list:
                    product_ve_quantity = m.split("-")
                    product_id = int(product_ve_quantity[0].strip())
                    quantity = int(product_ve_quantity[1])
                    product = Product.objects.get(pk=product_id)
                    data[product.product_name]=quantity
            else:
                data[product_and_quantity]=stok_ile_gelen_quantity

        representation['product'] = data

        return representation

    class Meta:
        model = Operation
        fields = "__all__"

class StockSerializer(DynamicFieldsCategorySerializer):
    warehouse = WarehouseSerializer(read_only=True, fields=['id', 'name'])
    product = ProductSerializer(read_only=True, fields=['id', 'product_name', 'price'])

    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.select_related('office', 'company').all(), source='warehouse', write_only=True
    )

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.select_related('company', 'category', 'unit_of_measure').all(), source='product', write_only=True
    )
    
    class Meta:
        model = Stock
        fields = "__all__"


class WarehouseRequestSerializer(DynamicFieldsCategorySerializer):
    warehouse = WarehouseSerializer(read_only=True, fields=['id', 'name'])
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.select_related('office', 'company').all(), source='warehouse', write_only=True
    )

    employee_who_sent_the_request = UserSerializer(read_only=True, fields=['id', 'fullname'])
    employee_who_sent_the_request_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.select_related(
                'company', 'office', 'section', 'position', 'team', 'employee_status', 'department'
            ).prefetch_related('user_permissions', 'groups').all(), source='employee_who_sent_the_request', write_only=True, required=False, allow_null=True
    )

    stok = StockSerializer(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        product_and_quantity = instance.product_and_quantity
        stok_list = list()
        
        if(product_and_quantity is not None):
            product_and_quantity_list = product_and_quantity.split(",")
            for m in product_and_quantity_list:
                stok_data = dict()
                product_ve_quantity = m.split("-")
                product_id = int(product_ve_quantity[0].strip())
                quantity = int(product_ve_quantity[1])
                try:
                    product = Product.objects.get(pk=product_id)
                except:
                    product=None
                try:
                    stok = Stock.objects.filter(product=product, warehouse=instance.warehouse)[0]
                    stok_data['id'] = stok.id
                    stok_data['product_id'] = stok.product.id
                    stok_data['product'] = stok.product.product_name
                    stok_data['price'] = stok.product.price
                    stok_data['stock_quantity'] = stok.quantity
                    stok_data['needed_quantity'] = quantity
                    stok_list.append(stok_data)
                except:
                    stok_list.append(stok_data)
        
        representation['product'] = stok_list

        return representation

    class Meta:
        model = WarehouseRequest
        fields = "__all__"
        read_only_fields = ('employee_who_sent_the_request', 'stok')