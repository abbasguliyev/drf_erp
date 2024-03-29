from rest_framework import serializers
from core.utils.base_serializer import DynamicFieldsCategorySerializer
from django.db.models import Sum, Q

from salary.models import (
    AdvancePayment,
    SalaryDeduction,
    Bonus,
    SalaryPunishment,
    SalaryView,
    PaySalary,
    MonthRange, SaleRange, CommissionInstallment, CommissionSaleRange, Commission,
    EmployeeActivityHistory
)

from account.api.serializers import UserSerializer
from account.api.selectors import user_list
from salary.api.selectors import employee_activity_history_list
from contract.api.selectors import demo_sales_list, contract_list
from contract import CONTINUING, CANCELLED


class AdvancePaymentSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=["id", "fullname"])
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='employee', write_only=True
    )

    class Meta:
        model = AdvancePayment
        fields = ('id', 'employee', 'employee_id',
                  'amount', 'note', 'date', 'salary_date', 'is_paid',)


class SalaryDeductionSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=["id", "fullname"])
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='employee', write_only=True
    )

    class Meta:
        model = SalaryDeduction
        fields = "__all__"


class SalaryPunishmentSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=["id", "fullname"])
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='employee', write_only=True
    )

    class Meta:
        model = SalaryPunishment
        fields = "__all__"


class BonusSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=["id", "fullname"])
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='employee', write_only=True
    )

    class Meta:
        model = Bonus
        fields = "__all__"


class PaySalarySerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = PaySalary
        fields = '__all__'
        read_only_fields = ('amount',)


class SalaryViewSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=[
                              'id', 'fullname', 'company', 'office', 'position', 'salary'])
    extra_data = serializers.SerializerMethodField()

    def get_extra_data(self, instance):
        month = instance.date.month
        year = instance.date.year

        qs = dict()
        qss = employee_activity_history_list().filter(salary_view=instance, activity_date__month = month, activity_date__year = year).last()
        total_working_day = user_list().filter(pk= instance.employee.id).aggregate(total_working_day=Sum('working_days__working_days_count', filter=Q(
            working_days__employee=instance.employee, working_days__date=instance.date)))
        continuing_sales = contract_list().filter(Q(group_leader=instance.employee) | Q(manager1=instance.employee) | Q(manager2=instance.employee), contract_status=CONTINUING, contract_date__month=month, contract_date__year=year).count()
        falling_sales = contract_list().filter(Q(group_leader=instance.employee) | Q(manager1=instance.employee) | Q(manager2=instance.employee), contract_status=CANCELLED, contract_date__month=month, contract_date__year=year).count()
            
        try:
            total_advancepayment = qss.advance_payment
        except:
            total_advancepayment = 0
        try:
            total_bonus = qss.bonus
        except:
            total_bonus = 0
        try:
            total_salarydeduction = qss.salary_deduction
        except:
            total_salarydeduction = 0
        try:
            total_salarypunishment = qss.salary_punishment
        except:
            total_salarypunishment = 0
        try:
            total_continuing_sales = continuing_sales
        except:
            total_continuing_sales = 0
        try:
            total_falling_sales = falling_sales
        except:
            total_falling_sales = 0


        if total_working_day.get("total_working_day") is None:
            total_working_day = 0
        else:
            total_working_day = total_working_day.get('total_working_day')

        qs['total_advancepayment'] = int(total_advancepayment)
        qs['total_bonus'] = int(total_bonus)
        qs['total_salarydeduction'] = int(total_salarydeduction)
        qs['total_salarypunishment'] = int(total_salarypunishment)
        qs['total_working_day'] = int(total_working_day)
        qs['total_continuing_sales'] = int(total_continuing_sales)
        qs['total_falling_sales'] = int(total_falling_sales)

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
    for_sale_range = CommissionSaleRangeSerializer(read_only=True, many=True)

    month_ranges = serializers.CharField(
        write_only=True, required=False, allow_blank=True)
    sale_ranges = serializers.CharField(
        write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Commission
        fields = (
            'id',
            'commission_name',
            'for_office',
            'cash',
            'for_team',
            'installment',
            'for_sale_range',
            'month_ranges',
            'sale_ranges',
            'creditor_per_cent'
        )

class EmployeeActivityHistorySerializer(serializers.ModelSerializer):
    salary_view = SalaryViewSerializer(read_only=True, fields=['id', 'employee', 'sale_quantity', 'commission_amount', 'final_salary', 'date'])
    extra_data = serializers.SerializerMethodField()

    def get_extra_data(self, instance):
        salary_view = instance.salary_view
        qs = dict()
        total_working_day = user_list().filter(pk= salary_view.employee.id).aggregate(total_working_day=Sum('working_days__working_days_count', filter=Q(
            working_days__employee=salary_view.employee, working_days__date=salary_view.date)))
        
        total_demo_count = demo_sales_list().filter(
            user=salary_view.employee, created_date__month=salary_view.date.month, created_date__year=salary_view.date.year
        ).aggregate(total_working_day=Sum('count'))

        if total_working_day.get("total_working_day") is None:
            total_working_day = 0
        else:
            total_working_day = total_working_day.get('total_working_day')

        if total_demo_count.get("total_demo_count") is None:
            total_demo_count = 0
        else:
            total_demo_count = total_demo_count.get('total_demo_count')

        qs['total_working_day'] = int(total_working_day)
        qs['total_demo_count'] = int(total_demo_count)

        return qs
    
    class Meta:
        model = EmployeeActivityHistory
        fields = '__all__'