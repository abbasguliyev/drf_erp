from rest_framework import serializers
from restAPI.core import DynamicFieldsCategorySerializer

from rest_framework.exceptions import ValidationError

from account.models import (
    User
)
from cashbox.models import HoldingCashbox, OfficeCashbox, CompanyCashbox
from restAPI.v1.cashbox.serializers import HoldingCashboxSerializer, OfficeCashboxSerializer, CompanyCashboxSerializer

from transfer.models import (
    TransferFromHoldingToCompany,
    TransferFromOfficeToCompany,
    TransferFromCompanyToHolding,
    TransferFromCompanyToOffices
)

from contract.models import Contract, ContractCreditor
from django.contrib.auth.models import Group


class TransferFromHoldingToCompanySerializer(DynamicFieldsCategorySerializer):
    executor = serializers.StringRelatedField()
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    cashbox = HoldingCashboxSerializer(read_only=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=HoldingCashbox.objects.all(), source='cashbox', write_only=True
    )

    cashbox = CompanyCashboxSerializer(read_only=True, many=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=CompanyCashbox.objects.all(), source='cashbox', many=True, write_only=True
    )

    class Meta:
        model = TransferFromHoldingToCompany
        fields = "__all__"
        read_only_fields = ('qalan_amount', 'previous_balance', 'subsequent_balance')


class TransferFromCompanyToHoldingSerializer(DynamicFieldsCategorySerializer):
    executor = serializers.StringRelatedField()
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    cashbox = CompanyCashboxSerializer(read_only=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=CompanyCashbox.objects.all(), source='cashbox', write_only=True
    )

    cashbox = HoldingCashboxSerializer(read_only=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=HoldingCashbox.objects.all(), source='cashbox', write_only=True
    )

    class Meta:
        model = TransferFromCompanyToHolding
        fields = "__all__"
        read_only_fields = ('qalan_amount', 'previous_balance', 'subsequent_balance')


class TransferFromOfficeToCompanySerializer(DynamicFieldsCategorySerializer):
    executor = serializers.StringRelatedField()
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    cashbox = OfficeCashboxSerializer(read_only=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=OfficeCashbox.objects.all(), source='cashbox', write_only=True
    )
    cashbox = CompanyCashboxSerializer(read_only=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=CompanyCashbox.objects.all(), source='cashbox', write_only=True
    )

    class Meta:
        model = TransferFromOfficeToCompany
        fields = "__all__"
        read_only_fields = ('qalan_amount', 'previous_balance', 'subsequent_balance')

class TransferFromCompanyToOfficesSerializer(DynamicFieldsCategorySerializer):
    executor = serializers.StringRelatedField()
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    cashbox = CompanyCashboxSerializer(read_only=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=CompanyCashbox.objects.all(), source='cashbox', write_only=True
    )

    cashbox = OfficeCashboxSerializer(read_only=True, many=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=OfficeCashbox.objects.all(), source='cashbox', many=True,  write_only=True
    )

    class Meta:
        model = TransferFromCompanyToOffices
        fields = "__all__"
        read_only_fields = ('qalan_amount', 'previous_balance', 'subsequent_balance')

