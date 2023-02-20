from rest_framework import serializers
from core.utils.base_serializer import DynamicFieldsCategorySerializer
from warehouse.api.selectors import warehouse_list
from warehouse.models import (
    Warehouse, 
    WarehouseRequest, 
    Stock,
    ChangeUnuselessOperation,
    HoldingWarehouse,
    WarehouseHistory
)

from company.models import (
    Company,
    Office,
)

from account.api.selectors import user_list
from account.api.serializers import UserSerializer, CustomerSerializer
from product.api.serializers import ProductSerializer
from product.api.selectors import product_list
from warehouse.api.selectors import holding_warehouse_list

from company.api.serializers import OfficeSerializer, CompanySerializer
from company.api.selectors import company_list, office_list

class WarehouseSerializer(DynamicFieldsCategorySerializer):
    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    office = OfficeSerializer(read_only=True, fields=['id', 'name', 'company'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=company_list(), source='company', write_only=True
    )
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=office_list(), source='office', write_only=True
    )

    class Meta:
        model = Warehouse
        fields = "__all__"

class StockSerializer(DynamicFieldsCategorySerializer):
    warehouse = WarehouseSerializer(read_only=True, fields=['id', 'name', 'company'])
    product = ProductSerializer(read_only=True, fields=['id', 'product_name', 'price', 'unit_of_measure'])

    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=warehouse_list(), source='warehouse', write_only=True
    )

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=product_list(), source='product', write_only=True
    )
    
    class Meta:
        model = Stock
        fields = "__all__"

class WarehouseRequestSerializer(DynamicFieldsCategorySerializer):
    warehouse = WarehouseSerializer(read_only=True, fields=['id', 'name', 'office'])
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=warehouse_list(), source='warehouse', write_only=True, required=False
    )

    employee_who_sent_the_request = UserSerializer(read_only=True, fields=['id', 'fullname'])
    employee_who_sent_the_request_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='employee_who_sent_the_request', write_only=True, required=False, allow_null=True
    )

    product_and_quantity = serializers.CharField(write_only=True)
    products_and_quantities = serializers.SerializerMethodField()

    def get_products_and_quantities(self, instance):
        products_and_quantity = instance.product_and_quantity
        products_and_quantity_list = products_and_quantity.split(',')
        wanted_prod_list = list()
        if(products_and_quantity is not None):
            for product_and_quantity in products_and_quantity_list:
                data = dict()
                new_list = product_and_quantity.split('-')
                product_id = new_list[0]
                quantity = int(new_list[1])
                product = product_list().filter(pk=product_id).last()
                holding_warehouse = holding_warehouse_list().filter(product=product).last()
                if holding_warehouse is not None:
                    data['product_in_holding_warehouse_id'] = holding_warehouse.id
                    data['product_in_holding_warehouse_quantity'] = holding_warehouse.useful_product_count
                else:
                    data['product_in_holding_warehouse_id'] = None
                    data['product_in_holding_warehouse_quantity'] = 0
                if product is not None:
                    data['id'] = product.id
                    data['product'] = product.product_name
                else:
                    data['id'] = None
                    data['product'] = None
                data['quantity'] = quantity
                wanted_prod_list.append(data)
        return wanted_prod_list

    class Meta:
        model = WarehouseRequest
        fields = "__all__"


class HoldingWarehouseSerializer(DynamicFieldsCategorySerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = HoldingWarehouse
        fields = '__all__'

class ChangeUnuselessOperationSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = ChangeUnuselessOperation
        fields = '__all__'

class WarehouseHistorySerializer(DynamicFieldsCategorySerializer):
    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    customer = CustomerSerializer(read_only=True, fields=['id', 'fullname'])
    executor = UserSerializer(read_only=True, fields=['id', 'fullname'])

    class Meta:
        model = WarehouseHistory
        fields = '__all__'