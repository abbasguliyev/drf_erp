import datetime

from rest_framework import serializers
from api.core import DynamicFieldsCategorySerializer
from django.db.models import Sum, Q, Window, F
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
        fields = ('id', 'employee', 'employee_id',
                  'amount', 'note', 'date', 'is_paid',)


class SalaryDeductionSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=["id", "fullname"])
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', write_only=True
    )

    class Meta:
        model = SalaryDeduction
        fields = "__all__"


class SalaryPunishmentSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=["id", "fullname"])
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', write_only=True
    )

    class Meta:
        model = SalaryPunishment
        fields = "__all__"


class BonusSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=["id", "fullname"])
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
    employee = UserSerializer(read_only=True, fields=[
                              'id', 'fullname', 'company', 'office', 'position', 'salary'])
    extra_data = serializers.SerializerMethodField()

    def get_extra_data(self, instance):
        month = instance.date.month
        year = instance.date.year

        qs = dict()
        qss = SalaryView.objects.filter(
            employee=instance.employee, date__month=month, date__year=year)
        total_advancepayment = qss.aggregate(total_advancepayment=Sum('employee__advancepayment__amount', filter=Q(
            employee__advancepayment__employee=instance.employee, employee__advancepayment__salary_date__month=month, employee__advancepayment__salary_date__year=year)))
        total_bonus = qss.aggregate(total_bonus=Sum('employee__bonus__amount', filter=Q(
            employee__bonus__employee=instance.employee, employee__bonus__salary_date__month=month, employee__bonus__salary_date__year=year)))
        total_salarydeduction = qss.aggregate(total_salarydeduction=Sum('employee__salarydeduction__amount', filter=Q(
            employee__salarydeduction__employee=instance.employee, employee__salarydeduction__salary_date__month=month, employee__salarydeduction__salary_date__year=year)))
        total_salarypunishment = qss.aggregate(total_salarypunishment=Sum('employee__salarypunishment__amount', filter=Q(
            employee__salarypunishment__employee=instance.employee, employee__salarypunishment__salary_date__month=month, employee__salarypunishment__salary_date__year=year)))
        total_working_day = qss.aggregate(total_working_day=Sum('employee__working_days__working_days_count', filter=Q(
            employee__working_days__employee=instance.employee, employee__working_days__date=instance.date)))

        if total_advancepayment.get("total_advancepayment") is None:
            total_advancepayment = 0
        else:
            total_advancepayment = total_advancepayment.get('total_advancepayment')
        if total_bonus.get("total_bonus") is None:
            total_bonus = 0
        else:
            total_bonus = total_bonus.get('total_bonus')
        if total_salarydeduction.get("total_salarydeduction") is None:
            total_salarydeduction = 0
        else:
            total_salarydeduction = total_salarydeduction.get('total_salarydeduction')

        if total_salarypunishment.get("total_salarypunishment") is None:
            total_salarypunishment = 0
        else:
            total_salarypunishment = total_salarypunishment.get('total_salarypunishment')
        if total_working_day.get("total_working_day") is None:
            total_working_day = 0
        else:
            total_working_day = total_working_day.get('total_working_day')

        qs['total_advancepayment'] = total_advancepayment
        qs['total_bonus'] = total_bonus
        qs['total_salarydeduction'] = total_salarydeduction
        qs['total_salarypunishment'] = total_salarypunishment
        qs['total_working_day'] = total_working_day
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

    month_ranges = serializers.CharField(
        write_only=True, required=False, allow_blank=True)
    sale_ranges = serializers.CharField(
        write_only=True, required=False, allow_blank=True)

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
