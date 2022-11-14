import datetime

from rest_framework import serializers
from api.core import DynamicFieldsCategorySerializer
from django.db.models import Sum, Count, Q
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

from holiday.models import EmployeeWorkingDay

from api.v1.account.serializers import UserSerializer

class AdvancePaymentSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=["id", "fullname"])
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.select_related(
            'company', 'office', 'section', 'position', 'team', 'employee_status', 'department'
        ).prefetch_related('user_permissions', 'groups').all(), source='employee', write_only=True
    )

    is_removed = serializers.BooleanField(write_only=True, default=False)
    confirm_remove = serializers.BooleanField(write_only=True, default=False)


    class Meta:
        model = AdvancePayment
        fields = ('id', 'employee', 'employee_id', 'amount', 'note', 'date', 'is_done', 'is_removed', 'confirm_remove')


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
        fields = ('employee', 'amount', 'note', 'date', 'salary_date')
        read_only_fields = ('amount',)

class SalaryViewSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=['id', 'fullname', 'company', 'office', 'position', 'salary'])
    salary_opr = serializers.SerializerMethodField('salary_opr_fn')
    employee_working_day = serializers.SerializerMethodField('employee_working_day_fn')

    def employee_working_day_fn(self, instance) -> int:
        try:
            working_day = EmployeeWorkingDay.objects.values_list('id', 'working_days_count', flat=True).get(employee=instance.employee, date=instance.date)
            count = working_day.working_days_count
        except:
            count = 0
        return count

    def salary_opr_fn(self, instance) -> float:
        month = instance.date.month
        year = instance.date.year
        qs = User.objects.select_related(
                'holding', 'company', 'office', 'section', 'position', 'team', 'employee_status', 'department'
            ).filter(pk=instance.employee.pk).aggregate(
            total_advancepayment = Sum('advancepayment__amount', filter=Q(advancepayment__date__month=month, advancepayment__date__year=year)),
            total_bonus = Sum('bonus__amount', filter=Q(bonus__date__month=month, bonus__date__year=year)),
            total_salarydeduction = Sum('salarydeduction__amount', filter=Q(salarydeduction__date__month=month, salarydeduction__date__year=year)),
            total_salarypunishment = Sum('salarypunishment__amount', filter=Q(salarypunishment__date__month=month, salarypunishment__date__year=year)),
        )
        if qs.get("total_advancepayment") is None:
            qs['total_advancepayment'] = 0
        if qs.get("total_bonus") is None:
            qs['total_bonus'] = 0
        if qs.get("total_salarydeduction") is None:
            qs['total_salarydeduction'] = 0
        if qs.get("total_salarypunishment") is None:
            qs['total_salarypunishment'] = 0
        return qs

    class Meta:
        model = SalaryView
        fields = (
            'id', 
            'employee', 
            'sale_quantity', 
            'commission_amount',
            'final_salary',
            'pay_date',
            'is_done', 
            'salary_opr',   
            'employee_working_day',
            'date'
        )

class SalaryOprSerializer(serializers.Serializer):
    total_bonus = serializers.FloatField(read_only=True)
    total_advancepayment = serializers.FloatField(read_only=True)
    total_salarydeduction = serializers.FloatField(read_only=True)
    total_salarypunishment = serializers.FloatField(read_only=True)
    total_working_day = serializers.IntegerField(read_only=True)


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
