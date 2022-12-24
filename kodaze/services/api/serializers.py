from rest_framework import serializers
from core.utils.base_serializer import DynamicFieldsCategorySerializer

from contract.models import (
    Contract, 
)
from services.models import (
    Service, 
    ServicePayment, 
    ServiceProductForContract
)
from company.models import Company
from account.api.serializers import CustomerSerializer, UserSerializer
from account.api.selectors import customer_list, user_list
from contract.api.serializers import ContractSerializer
from product.api.serializers import ProductSerializer
from product.api.selectors import product_list
from services.api.selectors import service_list


class ServiceSerializer(DynamicFieldsCategorySerializer):
    contract = ContractSerializer(read_only=True, fields=['id','company', 'office', 'product', 'group_leader', 'manager1', 'creditor_contracts', 'contract_date', 'gifts'])
    product = ProductSerializer(read_only=True, many=True, fields=['id', 'product_name', 'guarantee'])
    customer = CustomerSerializer(read_only=True, fields=['id', 'fullname', 'phone_number_1', 'phone_number_2', 'phone_number_3', 'phone_number_4', 'region', 'address'])
    
    service_creditor = UserSerializer(read_only=True, fields=['id', 'fullname'])
    operator = UserSerializer(read_only=True, fields=['id', 'fullname'])

    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.all(), source='contract', write_only=True, required=False, allow_null=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=product_list(), source='product', many=True, write_only=True
    )
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=customer_list(), source='customer', write_only=True, required=False, allow_null=True
    )

    service_creditor_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='service_creditor', write_only=True, required=False, allow_null=True
    )
    operator_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='operator', write_only=True, required=False, allow_null=True
    )

    is_auto = serializers.BooleanField(read_only=True)

    class Meta:
        model = Service
        fields = "__all__"

class ServicePaymentSerializer(DynamicFieldsCategorySerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=service_list(), source='service', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = ServicePayment
        fields = "__all__"

class ServiceProductForContractSerializer(serializers.ModelSerializer):
    company = ServiceSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ServiceProductForContract
        fields = '__all__'


class ServiceStatistikaSerializer(DynamicFieldsCategorySerializer):
    contract = ContractSerializer(read_only=True)
    product = ProductSerializer(read_only=True, many=True)

    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.all(), source='contract', write_only=True, required=False, allow_null=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=product_list(), source='product', many=True, write_only=True
    )

    is_auto = serializers.BooleanField(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        discount = 0
        discount += instance.discount
        try:
            discount_faizi = (discount * 100) / instance.total_amount_to_be_paid
        except:
            discount_faizi = 0
        representation['endrim_faizi'] = discount_faizi

        return representation

    class Meta:
        model = Service
        fields = "__all__"

