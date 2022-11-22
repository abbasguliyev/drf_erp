from rest_framework import serializers
from core.utils.base_serializer import DynamicFieldsCategorySerializer
from account.models import (
    User
)
from company.models import (
    Holding,
    Company,
    Office
)
from cashbox.models import (
    HoldingCashbox,
    CompanyCashbox,
    OfficeCashbox,
    CashFlow,
    HoldingCashboxOperation,
    CompanyCashboxOperation
)
from company.api.serializers import HoldingSerializer, OfficeSerializer, CompanySerializer
from account.api.serializers import UserSerializer, CustomerSerializer
from account.api.selectors import user_list

class HoldingCashboxSerializer(DynamicFieldsCategorySerializer):
    holding = HoldingSerializer(read_only=True, fields=['id', 'name'])
    holding_id = serializers.PrimaryKeyRelatedField(
        queryset=Holding.objects.all(), source='holding', write_only=True
    )

    class Meta:
        model = HoldingCashbox
        fields = "__all__"


class CompanyCashboxSerializer(DynamicFieldsCategorySerializer):
    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )

    class Meta:
        model = CompanyCashbox
        fields = "__all__"


class OfficeCashboxSerializer(DynamicFieldsCategorySerializer):
    office = OfficeSerializer(read_only=True, fields=['id', 'name'])
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.all(), source='office', write_only=True
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

    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )

    office = OfficeSerializer(read_only=True, fields=['id', 'name'])
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.all(), source='office', write_only=True, allow_null=True
    )


    class Meta:
        model = CompanyCashboxOperation
        fields = "__all__"

