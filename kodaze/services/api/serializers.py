from rest_framework import serializers
from core.utils.base_serializer import DynamicFieldsCategorySerializer

from contract.models import (
    Contract, 
)
from services.models import (
    Service, 
    ServicePayment, 
)

from product.models import (
    Product, 
)

from contract.api.serializers import ContractSerializer
from product.api.serializers import ProductSerializer

class ServiceSerializer(DynamicFieldsCategorySerializer):
    contract = ContractSerializer(read_only=True)
    product = ProductSerializer(read_only=True, many=True)

    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.all(), source='contract', write_only=True, required=False, allow_null=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', many=True, write_only=True
    )

    is_auto = serializers.BooleanField(read_only=True)

    class Meta:
        model = Service
        fields = "__all__"

class ServiceStatistikaSerializer(DynamicFieldsCategorySerializer):
    contract = ContractSerializer(read_only=True)
    product = ProductSerializer(read_only=True, many=True)

    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.all(), source='contract', write_only=True, required=False, allow_null=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', many=True, write_only=True
    )

    is_auto = serializers.BooleanField(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        discount = 0
        discount += float(instance.discount)
        try:
            discount_faizi = (discount * 100) / float(instance.total_amount_to_be_paid)
        except:
            discount_faizi = 0
        representation['endrim_faizi'] = discount_faizi

        return representation

    class Meta:
        model = Service
        fields = "__all__"

class ServicePaymentSerializer(DynamicFieldsCategorySerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source='service', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = ServicePayment
        fields = "__all__"

