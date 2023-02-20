from rest_framework import serializers
from core.utils.base_serializer import DynamicFieldsCategorySerializer

from cashbox.models import (
    HoldingCashbox,
    CompanyCashbox,
    OfficeCashbox,
    CashFlow,
    HoldingCashboxOperation,
    CompanyCashboxOperation,
    CostType
)
from company.api.serializers import HoldingSerializer, OfficeSerializer, CompanySerializer
from company.api.selectors import holding_list, company_list, office_list
from account.api.serializers import UserSerializer, CustomerSerializer
from account.api.selectors import user_list
from cashbox.api.selectors import office_cashbox_list, cost_type_list
from django.db.models import Sum, Q

class HoldingCashboxSerializer(DynamicFieldsCategorySerializer):
    holding = HoldingSerializer(read_only=True, fields=['id', 'name'])
    holding_id = serializers.PrimaryKeyRelatedField(
        queryset=holding_list(), source='holding', write_only=True
    )

    class Meta:
        model = HoldingCashbox
        fields = "__all__"


class CompanyCashboxSerializer(DynamicFieldsCategorySerializer):
    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=company_list(), source='company', write_only=True
    )
    offices_of_company_total_balance = serializers.SerializerMethodField()

    def get_offices_of_company_total_balance(self, instance):
        company = instance.company
        office_cashboxes = office_cashbox_list().filter(office__company = company).aggregate(
            total_balance=Sum('balance', filter=Q(office__company = company))
        )
        offices_total_balance = office_cashboxes.get('total_balance')
        if offices_total_balance is None:
            offices_total_balance = 0
        return int(offices_total_balance)

    class Meta:
        model = CompanyCashbox
        fields = "__all__"


class CostTypeSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = CostType
        fields = "__all__"

class OfficeCashboxSerializer(DynamicFieldsCategorySerializer):
    office = OfficeSerializer(read_only=True, fields=['id', 'name'])
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=office_list(), source='office', write_only=True
    )

    class Meta:
        model = OfficeCashbox
        fields = "__all__"


class CashFlowSerializer(DynamicFieldsCategorySerializer):
    holding = HoldingSerializer(read_only=True, fields=['id', 'name'])
    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    office = OfficeSerializer(read_only=True, fields=['id', 'name'])
    executor = UserSerializer(read_only=True, fields=["id", "fullname"])
    personal = UserSerializer(read_only=True, fields=["id", "fullname"])
    customer = CustomerSerializer(read_only=True, fields=["id", "fullname"])
    cost_type = CostTypeSerializer(read_only=True, fields=["id", "name"])
    
    class Meta:
        model = CashFlow
        fields = '__all__'

class HoldingCashboxOperationSerializer(DynamicFieldsCategorySerializer):
    executor = UserSerializer(read_only=True, fields=["id", "fullname"])
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='executor', write_only=True, required=False
    )

    personal = UserSerializer(read_only=True, fields=["id", "fullname"])
    personal_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='personal', write_only=True, required=False, allow_null=True
    )

    cost_type = CostTypeSerializer(read_only=True, fields=["id", "name"])
    cost_type_id = serializers.PrimaryKeyRelatedField(
        queryset=cost_type_list(), source='cost_type', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = HoldingCashboxOperation
        fields = "__all__"

class CompanyCashboxOperationSerializer(DynamicFieldsCategorySerializer):
    executor = UserSerializer(read_only=True, fields=["id", "fullname"])
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='executor', write_only=True, required=False
    )
    
    personal = UserSerializer(read_only=True, fields=["id", "fullname"])
    personal_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='personal', write_only=True, required=False, allow_null=True
    )

    cost_type = CostTypeSerializer(read_only=True, fields=["id", "name"])
    cost_type_id = serializers.PrimaryKeyRelatedField(
        queryset=cost_type_list(), source='cost_type', write_only=True, required=False, allow_null=True
    )


    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=company_list(), source='company', write_only=True
    )

    office = OfficeSerializer(read_only=True, fields=['id', 'name'])
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=office_list(), source='office', write_only=True, allow_null=True
    )


    class Meta:
        model = CompanyCashboxOperation
        fields = "__all__"