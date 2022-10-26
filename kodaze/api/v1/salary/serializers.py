from rest_framework import serializers
from api.core import DynamicFieldsCategorySerializer

from account.models import User

from salary.models import (
    AdvancePayment,
    SalaryDeduction,
    Bonus,
    SalaryPunishment,
    SalaryView,
    PaySalary,
    MonthRange, SaleRange, CommissionInstallment, CommissionSaleRange, Commission
)

from api.v1.account.serializers import UserSerializer

class AdvancePaymentSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=["id", "fullname"])
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.select_related(
            'company', 'office', 'section', 'position', 'team', 'employee_status', 'department'
        ).prefetch_related('user_permissions', 'groups').all(), source='employee', write_only=True
    )

    class Meta:
        model = AdvancePayment
        fields = "__all__"


class SalaryDeductionSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', write_only=True
    )

    class Meta:
        model = SalaryDeduction
        fields = "__all__"


class SalaryPunishmentSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', write_only=True
    )

    class Meta:
        model = SalaryPunishment
        fields = "__all__"


class BonusSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', write_only=True
    )

    class Meta:
        model = Bonus
        fields = "__all__"


class PaySalarySerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = PaySalary
        fields = ('employee', 'amount', 'note', 'salary_date')
        read_only_fields = ('amount',)

class SalaryViewSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', write_only=True
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        month = instance.date.month

        advancepayment = AdvancePayment.objects.filter(employee=instance.employee, date__month=month)
        bonus = Bonus.objects.filter(employee=instance.employee, date__month=month)
        salarydeduction = SalaryDeduction.objects.filter(employee=instance.employee, date__month=month)
        salarypunishment = SalaryPunishment.objects.filter(employee=instance.employee, date__month=month)

        total_advancepayment = 0
        total_bonus = 0
        total_salarydeduction = 0
        total_salarypunishment = 0

        for a in advancepayment:
            total_advancepayment += a.amount

        for b in bonus:
            total_bonus += b.amount

        for k in salarydeduction:
            total_salarydeduction += k.amount

        for p in salarypunishment:
            total_salarypunishment += p.amount

        representation['advancepayment'] = total_advancepayment
        representation['bonus'] = total_bonus
        representation['salarydeduction'] = total_salarydeduction
        representation['salarypunishment'] = total_salarypunishment

        return representation

    class Meta:
        model = SalaryView
        fields = '__all__'
        read_only_fields = ('advancepayment', 'bonus', 'salarydeduction', 'salarypunishment')


class MonthRangeSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = MonthRange
        fields = '__all__'


class SaleRangeSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = SaleRange
        fields = '__all__'


class CommissionInstallmentSerializer(DynamicFieldsCategorySerializer):
    month_range = MonthRangeSerializer(read_only=True)
    month_range_id = serializers.PrimaryKeyRelatedField(
        queryset=MonthRange.objects.all(), source="month_range", write_only=True
    )
    class Meta:
        model = CommissionInstallment
        fields = '__all__'


class CommissionSaleRangeSerializer(DynamicFieldsCategorySerializer):
    sale_range = SaleRangeSerializer(read_only=True)
    sale_range_id = serializers.PrimaryKeyRelatedField(
        queryset=SaleRange.objects.all(), source="sale_range", write_only=True
    )
    class Meta:
        model = CommissionSaleRange
        fields = '__all__'


class CommissionSerializer(DynamicFieldsCategorySerializer):
    installment = CommissionInstallmentSerializer(read_only=True, many=True)
    # installment_id = serializers.PrimaryKeyRelatedField(
    #     queryset=CommissionInstallment.objects.select_related('month_range').all(),
    #     source="installment", write_only=True, many=True
    # )

    for_sale_range = CommissionSaleRangeSerializer(read_only=True, many=True)
    # for_sale_range_id = serializers.PrimaryKeyRelatedField(
    #     queryset=CommissionSaleRange.objects.select_related('sale_range').all(),
    #     source="for_sale_range", write_only=True, many=True
    # )

    month_ranges = serializers.CharField(write_only=True, required=False, allow_blank=True)
    sale_ranges = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Commission
        fields = (
            'commission_name',
            'for_office',
            'cash',
            'for_team',
            'installment',
            'for_sale_range',
            'month_ranges',
            'sale_ranges',
        )
