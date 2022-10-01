from rest_framework import serializers
from restAPI.core import DynamicFieldsCategorySerializer
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
    CashFlow
)
from restAPI.v1.company.serializers import HoldingSerializer, OfficeSerializer, CompanySerializer

class HoldingCashboxSerializer(DynamicFieldsCategorySerializer):
    holding = HoldingSerializer(read_only=True)
    holding_id = serializers.PrimaryKeyRelatedField(
        queryset=Holding.objects.all(), source='holding', write_only=True
    )

    class Meta:
        model = HoldingCashbox
        fields = "__all__"


class CompanyCashboxSerializer(DynamicFieldsCategorySerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )

    class Meta:
        model = CompanyCashbox
        fields = "__all__"


class OfficeCashboxSerializer(DynamicFieldsCategorySerializer):
    office = OfficeSerializer(read_only=True)
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.all(), source='office', write_only=True
    )

    class Meta:
        model = OfficeCashbox
        fields = "__all__"


class CashFlowSerializer(DynamicFieldsCategorySerializer):
    holding = HoldingSerializer(read_only=True)
    holding_id = serializers.PrimaryKeyRelatedField(
        queryset=Holding.objects.all(), source='holding', write_only=True, required=False, allow_null=True
    )

    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True, required=False, allow_null=True
    )

    office = OfficeSerializer(read_only=True)
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.all(), source='office', write_only=True, required=False, allow_null=True
    )

    executor = serializers.StringRelatedField()
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    
    class Meta:
        model = CashFlow
        fields = '__all__'
