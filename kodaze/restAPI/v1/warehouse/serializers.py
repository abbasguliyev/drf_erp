from rest_framework import serializers
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

from restAPI.v1.account.serializers import UserSerializer
from restAPI.v1.product.serializers import ProductSerializer

from restAPI.v1.company.serializers import OfficeSerializer, CompanySerializer

class WarehouseSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    office = OfficeSerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.all(), source='office', write_only=True
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

class OperationSerializer(serializers.ModelSerializer):
    executor = UserSerializer(read_only=True)
    shipping_warehouse = WarehouseSerializer(read_only=True)
    receiving_warehouse = WarehouseSerializer(read_only=True)

    shipping_warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), source="shipping_warehouse", write_only=True, required= True
    )
    receiving_warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), source="receiving_warehouse", write_only=True, required= True
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

class StockSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), source='warehouse', write_only=True
    )

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    
    class Meta:
        model = Stock
        fields = "__all__"


class WarehouseRequestSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), source='warehouse', write_only=True
    )

    employee_who_sent_the_request = UserSerializer(read_only=True)
    employee_who_sent_the_request_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee_who_sent_the_request', write_only=True, required=False, allow_null=True
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
                product = Product.objects.get(pk=product_id)
                try:
                    stok = Stock.objects.filter(product=product, warehouse=instance.warehouse)[0]
                    stok_data['id'] = stok.id
                    stok_data['product_id'] = stok.product.id
                    stok_data['product'] = stok.product.product_name
                    stok_data['price'] = stok.product.price
                    stok_data['quantity'] = stok.quantity
                    stok_data['quantityi'] = quantity
                    stok_list.append(stok_data)
                except:
                    stok_list.append(stok_data)
        
        representation['product'] = stok_list

        return representation

    class Meta:
        model = WarehouseRequest
        fields = "__all__"
        read_only_fields = ('employee_who_sent_the_request', 'stok')