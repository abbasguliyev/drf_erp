from rest_framework import serializers
from core.utils.base_serializer import DynamicFieldsCategorySerializer
from warehouse.api.selectors import warehouse_list, stock_list
from warehouse.models import (
    Operation, 
    Warehouse, 
    WarehouseRequest, 
    Stock,
    ChangeUnuselessOperation,
    HoldingWarehouse
)

from company.models import (
    Company,
    Office,
)

from account.api.selectors import user_list
from account.api.serializers import UserSerializer
from product.api.serializers import ProductSerializer
from product.api.selectors import product_list

from company.api.serializers import OfficeSerializer, CompanySerializer

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

class StockSerializer(DynamicFieldsCategorySerializer):
    warehouse = WarehouseSerializer(read_only=True, fields=['id', 'name'])
    product = ProductSerializer(read_only=True, fields=['id', 'product_name', 'price'])

    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=warehouse_list(), source='warehouse', write_only=True
    )

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=product_list(), source='product', write_only=True
    )

    useful_product_count = serializers.SerializerMethodField()

    def get_useful_product_count(self, instance) -> int:
        instance.product

    
    class Meta:
        model = Stock
        fields = "__all__"


class OperationSerializer(DynamicFieldsCategorySerializer):
    executor = UserSerializer(read_only=True, fields = ['id', 'fullname'])
    shipping_warehouse = WarehouseSerializer(read_only=True, fields = ['id', 'name'])
    receiving_warehouse = WarehouseSerializer(read_only=True, fields = ['id', 'name'])

    shipping_warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=warehouse_list(), source="shipping_warehouse", write_only=True, required= True
    )
    receiving_warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=warehouse_list(), source="receiving_warehouse", write_only=True, required= True
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
                    product = product_list().filter(pk=product_id).last()
                    data[product.product_name]=quantity
            else:
                data[product_and_quantity]=stok_ile_gelen_quantity

        representation['product'] = data

        return representation

    class Meta:
        model = Operation
        fields = "__all__"

class WarehouseRequestSerializer(DynamicFieldsCategorySerializer):
    warehouse = WarehouseSerializer(read_only=True, fields=['id', 'name'])
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=warehouse_list(), source='warehouse', write_only=True
    )

    employee_who_sent_the_request = UserSerializer(read_only=True, fields=['id', 'fullname'])
    employee_who_sent_the_request_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='employee_who_sent_the_request', write_only=True, required=False, allow_null=True
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
                    product = product_list().filter(pk=product_id).last()
                except:
                    product=None
                try:
                    stok = stock_list().filter(product=product, warehouse=instance.warehouse)[0]
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


class HoldingWarehouseSerializer(DynamicFieldsCategorySerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = HoldingWarehouse
        fields = '__all__'

class ChangeUnuselessOperationSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = ChangeUnuselessOperation
        fields = '__all__'