from rest_framework import serializers
from api.core import DynamicFieldsCategorySerializer

from account.models import (
    User
)

from api.v1.account.serializers import UserSerializer

from transfer.models import (
    HoldingTransfer,
    CompanyTransfer,
    OfficeTransfer,
)

from company.models import Company, Office
from api.v1.company.serializers import CompanySerializer, OfficeSerializer

class HoldingTransferSerializer(DynamicFieldsCategorySerializer):
    executor = UserSerializer(read_only=True, fields = ['id', 'username','fullname'])
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    sending_company = CompanySerializer(read_only=True, fields = ['name'])
    sending_company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='sending_company', write_only=True, allow_null=True
    )

    receiving_company = CompanySerializer(read_only=True, fields = ['name'])
    receiving_company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='receiving_company',  write_only=True, allow_null=True
    )

    class Meta:
        model = HoldingTransfer
        fields = "__all__"

class CompanyTransferSerializer(DynamicFieldsCategorySerializer):
    executor = UserSerializer(read_only=True, fields = ['id', 'username','fullname'])
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    company = CompanySerializer(read_only=True, fields = ['name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )

    sending_office = OfficeSerializer(read_only=True, fields = ['name'])
    sending_office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.select_related('company').all(), source='sending_office', write_only=True, allow_null=True
    )

    receiving_office = OfficeSerializer(read_only=True, fields = ['name'])
    receiving_office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.select_related('company').all(), source='receiving_office',  write_only=True, allow_null=True
    )

    class Meta:
        model = CompanyTransfer
        fields = "__all__"

class OfficeTransferSerializer(DynamicFieldsCategorySerializer):
    executor = UserSerializer(read_only=True, fields = ['id', 'username','fullname'])
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    company = CompanySerializer(read_only=True, fields = ['name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )

    sending_office = OfficeSerializer(read_only=True, fields = ['name'])
    sending_office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.select_related('company').all(), source='sending_office', write_only=True
    )

    receiving_office = OfficeSerializer(read_only=True, fields = ['name'])
    receiving_office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.select_related('company').all(), source='receiving_office',  write_only=True
    )

    class Meta:
        model = OfficeTransfer
        fields = "__all__"
