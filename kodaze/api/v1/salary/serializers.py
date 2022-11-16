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

    class Meta:
        model = AdvancePayment
        fields = ('id', 'employee', 'employee_id', 'amount', 'note', 'date', 'is_done',)


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
    extra_data = serializers.SerializerMethodField('extra_data_fn')

    def extra_data_fn(self, instance) -> float:
        month = instance.date.month
        year = instance.date.year
       
        qs = SalaryView.objects.select_related('employee').filter(employee=instance.employee, date=instance.date).aggregate(
            total_advancepayment = Sum('employee__advancepayment__amount', filter=Q(employee__advancepayment__date__month=month, employee__advancepayment__date__year=year)),
            total_bonus = Sum('employee__bonus__amount', filter=Q(employee__bonus__date__month=month, employee__bonus__date__year=year)),
            total_salarydeduction = Sum('employee__salarydeduction__amount', filter=Q(employee__salarydeduction__date__month=month, employee__salarydeduction__date__year=year)),
            total_salarypunishment = Sum('employee__salarypunishment__amount', filter=Q(employee__salarypunishment__date__month=month, employee__salarypunishment__date__year=year)),
            total_working_day = Sum('employee__working_days__working_days_count', filter=Q(employee__working_days__date=instance.date)),
        )
        if qs.get("total_advancepayment") is None:
            qs['total_advancepayment'] = 0
        if qs.get("total_bonus") is None:
            qs['total_bonus'] = 0
        if qs.get("total_salarydeduction") is None:
            qs['total_salarydeduction'] = 0
        if qs.get("total_salarypunishment") is None:
            qs['total_salarypunishment'] = 0
        if qs.get("total_working_day") is None:
            qs['total_working_day'] = 0
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
            'extra_data',   
            'date'
        )

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
