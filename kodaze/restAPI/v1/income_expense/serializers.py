from rest_framework import serializers

from account.models import (
    User
)

from income_expense.models import (
    HoldingCashboxIncome,
    HoldingCashboxExpense,
    OfficeCashboxIncome,
    OfficeCashboxExpense,
    CompanyCashboxIncome,
    CompanyCashboxExpense
)

from cashbox.models import HoldingCashbox, OfficeCashbox, CompanyCashbox

from restAPI.v1.cashbox.serializers import (
    HoldingCashboxSerializer, 
    OfficeCashboxSerializer, 
    CompanyCashboxSerializer
)

class HoldingCashboxIncomeSerializer(serializers.ModelSerializer):
    executor = serializers.StringRelatedField()
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    cashbox = HoldingCashboxSerializer(read_only=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=HoldingCashbox.objects.all(), source='cashbox', write_only=True
    )

    class Meta:
        model = HoldingCashboxIncome
        fields = "__all__"
        read_only_fields = ('previous_balance', 'subsequent_balance')


class HoldingCashboxExpenseSerializer(serializers.ModelSerializer):
    executor = serializers.StringRelatedField()
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    cashbox = HoldingCashboxSerializer(read_only=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=HoldingCashbox.objects.all(), source='cashbox', write_only=True
    )

    class Meta:
        model = HoldingCashboxExpense
        fields = "__all__"
        read_only_fields = ('previous_balance', 'subsequent_balance')


class CompanyCashboxIncomeSerializer(serializers.ModelSerializer):
    executor = serializers.StringRelatedField()
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    cashbox = CompanyCashboxSerializer(read_only=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=CompanyCashbox.objects.all(), source='cashbox', write_only=True
    )

    class Meta:
        model = CompanyCashboxIncome
        fields = "__all__"
        read_only_fields = ('previous_balance', 'subsequent_balance')


class CompanyCashboxExpenseSerializer(serializers.ModelSerializer):
    executor = serializers.StringRelatedField()
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    cashbox = CompanyCashboxSerializer(read_only=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=CompanyCashbox.objects.all(), source='cashbox', write_only=True
    )

    class Meta:
        model = CompanyCashboxExpense
        fields = "__all__"
        read_only_fields = ('previous_balance', 'subsequent_balance')


class OfficeCashboxIncomeSerializer(serializers.ModelSerializer):
    executor = serializers.StringRelatedField()
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    cashbox = OfficeCashboxSerializer(read_only=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=OfficeCashbox.objects.all(), source='cashbox', write_only=True
    )

    class Meta:
        model = OfficeCashboxIncome
        fields = '__all__'
        read_only_fields = ('previous_balance', 'subsequent_balance')


class OfficeCashboxExpenseSerializer(serializers.ModelSerializer):
    executor = serializers.StringRelatedField()
    executor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='executor', write_only=True, required=False, allow_null=True
    )
    cashbox = OfficeCashboxSerializer(read_only=True)
    cashbox_id = serializers.PrimaryKeyRelatedField(
        queryset=OfficeCashbox.objects.all(), source='cashbox', write_only=True
    )

    class Meta:
        model = OfficeCashboxExpense
        fields = '__all__'
        read_only_fields = ('previous_balance', 'subsequent_balance')