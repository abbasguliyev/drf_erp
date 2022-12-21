import datetime
from rest_framework import serializers
from company.api.serializers import OfficeSerializer, CompanySerializer, SectionSerializer

from account.api.serializers import CustomerSerializer, UserSerializer
from account.api.selectors import user_list, customer_list
from product.api.serializers import ProductSerializer
from core.utils.base_serializer import DynamicFieldsCategorySerializer
from product.api.selectors import product_list

from contract.models import (
    ContractGift, 
    ContractCreditor,
    Contract, 
    Installment,  
    ContractChange, 
    DemoSales
)

from services.models import (
    Service,
)

from product.models import (
    Product,
)

from company.models import (
    Company,
    Office,
)

class ServiceContractSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = Service
        fields = ['id', 'is_done']

class ContractSerializer(DynamicFieldsCategorySerializer):
    group_leader = UserSerializer(read_only=True, fields=["id", "fullname"])
    manager1 = UserSerializer(read_only=True, fields=["id", "fullname"])
    manager2 = UserSerializer(read_only=True, fields=["id", "fullname"])
    customer = CustomerSerializer(read_only=True, fields=["id", "fullname", "phone_number_1", "phone_number_2", "region", "address"])
    product = ProductSerializer(read_only=True, fields=["id", "product_name", "price"])
    company = CompanySerializer(read_only=True, fields=["id", "name"])
    office = OfficeSerializer(read_only=True, fields=["id", "name"])

    cancelled_date = serializers.DateField(read_only=True)
    is_remove = serializers.BooleanField(read_only=True)
    debt_finished = serializers.BooleanField(read_only=True)

    service_contract = ServiceContractSerializer(read_only=True, many=True)

    group_leader_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='group_leader', write_only=True, required=False, allow_null=True
    )
    manager1_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='manager1', write_only=True, required=False, allow_null=True
    )
    manager2_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='manager2', write_only=True, required=False, allow_null=True
    )
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=customer_list(), source='customer', write_only=True, required=False, allow_null=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=product_list(), source='product', write_only=True, required=False, allow_null=True
    )
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True, required=False, allow_null=True
    )

    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.select_related('company').all(), source='office', write_only=True, required=False, allow_null=True
    )

    contract_created_date = serializers.DateField(read_only=True)

    def create(self, validated_data):
        contract_date = validated_data.get('contract_date')
        initial_payment_date = validated_data.get('initial_payment_date')
        payment_style = validated_data.get('payment_style')
        initial_payment = validated_data.get('initial_payment')
        if contract_date == None:
            validated_data['contract_date'] = datetime.date.today()
        if payment_style == "KREDİT":
            if initial_payment is not None:
                if initial_payment > 0:
                    if initial_payment_date == None:
                        validated_data['initial_payment_date'] = datetime.date.today()
        return super(ContractSerializer, self).create(validated_data)

    class Meta:
        model = Contract
        fields = "__all__"
        read_only_fields = (
            'total_amount', 
            'initial_payment_status',
            'initial_payment_debt_status',
            'service_contract',
            'remaining_debt',
            'pdf',
            'pdf2',
            'cancelled_date',
            'contract_created_date',
            'is_remove',
            'debt_finished'
        )

class ContractGiftSerializer(DynamicFieldsCategorySerializer):
    product = ProductSerializer(read_only=True, fields=["id", "product_name", "price"])
    contract = ContractSerializer(read_only=True, fields=["id", "customer"])

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=product_list(), source='product', write_only=True, allow_null=True
    )

    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.select_related(
                    'group_leader', 
                    'manager1', 
                    'manager2', 
                    'customer', 
                    'product', 
                    'company', 
                    'office', 
                ).all(), source='contract', write_only=True
    )

    gift_date = serializers.DateField(read_only=True)
    products_and_quantity = serializers.CharField(write_only=True)

    class Meta:
        model = ContractGift
        fields = "__all__"
        read_only_fields = ('gift_date',)


class InstallmentSerializer(DynamicFieldsCategorySerializer):
    contract = ContractSerializer(read_only=True, fields=["id", "customer", "company", "office", "contract_date", "remaining_debt"])
    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.select_related(
                    'group_leader', 
                    'manager1', 
                    'manager2', 
                    'customer', 
                    'product', 
                    'company', 
                    'office', 
                ).all(), source='contract', write_only=True
    )

    contract_creditor = serializers.SerializerMethodField()

    def get_contract_creditor(self, instance):
        contract = instance.contract
        creditor_contracts = ContractCreditor.objects.select_related('creditor', 'contract').filter(contract=contract).first()
        creditor = None
        if creditor_contracts is not None:
            creditor = dict()
            user_creditor = creditor_contracts.creditor
            creditor_contracts_id = creditor_contracts.id
            creditor_fullname = user_creditor.fullname

            creditor['id'] = creditor_contracts_id
            creditor['creditor_fullname'] = creditor_fullname
        return creditor
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     qalan_ay_quantityi = 0
    #     odenmeyen_installmentler = Installment.objects.filter(contract=instance.contract, payment_status="ÖDƏNMƏYƏN").exclude(conditional_payment_status="BURAXILMIŞ AY")
    #     qalan_ay_quantityi = len(odenmeyen_installmentler)
    #     representation['qalan_ay_quantityi'] = qalan_ay_quantityi

    #     return representation

    class Meta:
        model = Installment
        fields = "__all__"
        read_only_fields = ('last_month', 'month_no')

class ContractChangeSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = ContractChange
        fields = "__all__"

class DemoSalesSerializer(DynamicFieldsCategorySerializer):
    user = UserSerializer(read_only=True, fields=["id", "fullname"])
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='user', write_only=True, required=False, allow_null=True
    )
    sale_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = DemoSales
        fields = "__all__"
        read_only_fields = ('sale_count',)


class ContractCreditorSerializer(DynamicFieldsCategorySerializer):
    contract = ContractSerializer(read_only=True, fields=["id", "customer", "contract_date"])
    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=Contract.objects.select_related(
                    'group_leader', 
                    'manager1', 
                    'manager2', 
                    'customer', 
                    'product', 
                    'company', 
                    'office', 
                ).all(), source='contract', write_only=True
    )
    creditor = UserSerializer(read_only=True, fields=["id", "fullname"])
    creditor_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='creditor', write_only=True
    )
    class Meta:
        model = ContractCreditor
        fields = '__all__'