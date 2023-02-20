import datetime
from rest_framework import serializers
from core.utils.base_serializer import DynamicFieldsCategorySerializer
from company.models import Office
from company.api.serializers import OfficeSerializer, CompanySerializer
from company.api.selectors import company_list, office_list
from account.api.serializers import CustomerSerializer, UserSerializer, RegionSerializer
from account.api.selectors import user_list, customer_list, region_list
from product.api.serializers import ProductSerializer
from product.api.selectors import product_list

from contract.models import (
    ContractGift, 
    ContractCreditor,
    Contract, 
    Installment,  
    DemoSales
)
from contract.api.selectors import contract_list, contract_creditor_list, installment_list

from services.models import (
    Service,
)

class ServiceContractSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = Service
        fields = ['id', 'is_done']

class OldContractSerializer(DynamicFieldsCategorySerializer):
    product = ProductSerializer(read_only=True, fields=["id", "product_name", "price"])
    
    class Meta:
        model = Contract
        fields = [
            "id", "address", "product", "product_quantity", "total_amount", 
            "contract_date", "is_holding_contract", "remaining_debt", "loan_term", 
            "discount", "initial_payment", "paid_initial_payment", "initial_payment_debt", 
            "paid_initial_payment_debt", "initial_payment_date", "initial_payment_paid_date", 
            "initial_payment_debt_date", "initial_payment_debt_paid_date", "note", 
            "payment_style", "intervention_product_status", "intervention_date", 
            "contract_change_date"
        ]

class ContractSerializer(DynamicFieldsCategorySerializer):
    group_leader = UserSerializer(read_only=True, fields=["id", "fullname"])
    manager1 = UserSerializer(read_only=True, fields=["id", "fullname"])
    manager2 = UserSerializer(read_only=True, fields=["id", "fullname"])
    customer = CustomerSerializer(read_only=True, fields=["id", "fullname", "phone_number_1", "phone_number_2", "region", "address"])
    product = ProductSerializer(read_only=True, fields=["id", "product_name", "price"])
    region = RegionSerializer(read_only=True)
    company = CompanySerializer(read_only=True, fields=["id", "name"])
    office = OfficeSerializer(read_only=True, fields=["id", "name"])
    is_holding_contract = serializers.BooleanField(read_only=True)
    intervention_date = serializers.DateField(read_only=True)
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
        queryset=company_list(), source='company', write_only=True, required=False, allow_null=True
    )

    office_id = serializers.PrimaryKeyRelatedField(
        queryset=office_list(), source='office', write_only=True, required=False, allow_null=True
    )

    region_id = serializers.PrimaryKeyRelatedField(
        queryset=region_list(), source='region', write_only=True, required=True
    )

    old_contract = OldContractSerializer(read_only=True)
    old_contract_id = serializers.PrimaryKeyRelatedField(
        queryset=contract_list(), source='old_contract', write_only=True
    )

    contract_created_date = serializers.DateField(read_only=True)
    creditor = serializers.SerializerMethodField()
    current_installment = serializers.SerializerMethodField()

    def get_creditor(self, instance):
        contract = instance
        creditor_contracts = contract_creditor_list().filter(contract=contract).last()
        creditor = None
        if creditor_contracts is not None:
            creditor = dict()
            user_creditor = creditor_contracts.creditor
            creditor_contracts_id = creditor_contracts.id
            creditor_id = user_creditor.id
            creditor_fullname = user_creditor.fullname

            creditor['id'] = creditor_contracts_id
            creditor['user_id'] = creditor_id
            creditor['fullname'] = creditor_fullname
        return creditor

    def get_current_installment(self, instance):
        now = datetime.date.today()
        installment = installment_list().filter(contract=instance, date__month=now.month).last()
        if installment is not None:
            current_installment = dict()
            current_installment['id'] = installment.id
            current_installment['month_no'] = installment.month_no
            current_installment['payment_status'] = installment.payment_status
            current_installment['delay_status'] = installment.delay_status
        else:
            current_installment = None
        return current_installment

    class Meta:
        model = Contract
        fields = "__all__"

class ContractCreateSerializer(DynamicFieldsCategorySerializer):
    is_holding_contract = serializers.BooleanField(read_only=True)
    intervention_date = serializers.DateField(read_only=True)
    is_remove = serializers.BooleanField(read_only=True)
    debt_finished = serializers.BooleanField(read_only=True)
    region = serializers.PrimaryKeyRelatedField(
        queryset=region_list(), write_only=True, required=True
    )
    address = serializers.CharField(write_only=True, required=True)
    customer = serializers.PrimaryKeyRelatedField(
        queryset=customer_list(), write_only=True, required=True
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=product_list(), write_only=True, required=True
    )
    
    class Meta:
        model = Contract
        fields = "__all__"

class ContractGiftSerializer(DynamicFieldsCategorySerializer):
    product = ProductSerializer(read_only=True, fields=["id", "product_name", "price"])
    contract = ContractSerializer(read_only=True, fields=["id", "customer"])

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=product_list(), source='product', write_only=True, allow_null=True
    )

    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=contract_list(), source='contract', write_only=True
    )

    gift_date = serializers.DateField(read_only=True)

    class Meta:
        model = ContractGift
        fields = "__all__"


class InstallmentSerializer(DynamicFieldsCategorySerializer):
    contract = ContractSerializer(read_only=True, fields=["id", "customer", "company", "office", "contract_date", "remaining_debt", "address", "region"])
    contract_id = serializers.PrimaryKeyRelatedField(
        queryset=contract_list(), source='contract', write_only=True
    )
    note = serializers.CharField(required=False,allow_null=True)
    contract_creditor = serializers.SerializerMethodField()

    def get_contract_creditor(self, instance):
        contract = instance.contract
        creditor_contracts = contract_creditor_list().filter(contract=contract).first()
        creditor = None
        if creditor_contracts is not None:
            creditor = dict()
            user_creditor = creditor_contracts.creditor
            creditor_contracts_id = creditor_contracts.id
            creditor_fullname = user_creditor.fullname

            creditor['id'] = creditor_contracts_id
            creditor['fullname'] = creditor_fullname
        return creditor
    
    class Meta:
        model = Installment
        fields = "__all__"
        read_only_fields = ('last_month', 'month_no')


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
        queryset=contract_list(), source='contract', write_only=True
    )
    creditor = UserSerializer(read_only=True, fields=["id", "fullname"])
    creditor_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='creditor', write_only=True
    )
    class Meta:
        model = ContractCreditor
        fields = '__all__'