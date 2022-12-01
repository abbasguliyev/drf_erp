from rest_framework import serializers
from core.utils.base_serializer import DynamicFieldsCategorySerializer

from holiday.models import (
    EmployeeWorkingDay,
    EmployeeHolidayHistory,
    EmployeeHoliday,
    HolidayOperation,
    EmployeeDayOff,
    EmployeeDayOffHistory,
    EmployeeDayOffOperation
)

from django.db.models import Sum, Q

from company.models import Company, Office

from account.api.serializers import UserSerializer
from account.api.selectors import user_list
from holiday.api.selectors import employee_day_off_list, employee_holiday_list

from company.api.serializers import (
    CompanySerializer,
    OfficeSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeWorkingDaySerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=['id', 'username', 'fullname', 'company', 'office', 'position', 'salary'])
    extra_data = serializers.SerializerMethodField()

    def get_extra_data(self, instance):
        emp = instance.employee
        qs = dict()
        total_holiday = employee_holiday_list().filter(employee = emp, holiday_date__month=instance.date.month, holiday_date__year=instance.date.year).count()
        total_payed_days_off = employee_day_off_list().filter(employee = emp, is_paid=True, day_off_date__month=instance.date.month, day_off_date__year=instance.date.year).count()
        total_unpayed_days_off = employee_day_off_list().filter(employee = emp, is_paid=False, day_off_date__month=instance.date.month, day_off_date__year=instance.date.year).count()

        qs['total_holiday'] = total_holiday
        qs['total_payed_days_off'] = total_payed_days_off
        qs['total_unpayed_days_off'] = total_unpayed_days_off

        return qs

    class Meta:
        model = EmployeeWorkingDay
        fields = '__all__'

class EmployeeHolidayHistorySerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=['id', 'username', 'fullname'])
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='employee', write_only=True,
    )

    day_count = serializers.SerializerMethodField()
    holiday_dates = serializers.SerializerMethodField()

    def get_day_count(self, instance):
        holiday_count = employee_holiday_list().filter(history = instance).count()
        return holiday_count

    def get_holiday_dates(self,instance):
        qs = list()
        holidays = employee_holiday_list().filter(history = instance)
        [qs.append(holiday.holiday_date) for holiday in holidays]
        return qs

    class Meta:
        model = EmployeeHolidayHistory
        fields = '__all__'

class EmployeeHolidaySerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = EmployeeHoliday
        fields = '__all__'

class HolidayOperationSerializer(DynamicFieldsCategorySerializer):
    person_on_duty = UserSerializer(read_only=True, many=True, fields=['id', 'username', 'fullname'])
    person_on_duty_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='person_on_duty', many=True, write_only=True, allow_empty=True
    )

    company = CompanySerializer(read_only=True, allow_null=True, fields=['id', 'name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True, allow_null=True,
    )

    office = OfficeSerializer(read_only=True, allow_null=True, fields=['id', 'name'])
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.select_related('company').all(), source='office', allow_null=True, write_only=True
    )

    class Meta:
        model = HolidayOperation
        fields = '__all__'

class EmployeeDayOffHistorySerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields=['id', 'username', 'fullname'])
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='employee', write_only=True,
    )

    paid_day_count = serializers.SerializerMethodField()
    unpaid_day_count = serializers.SerializerMethodField()
    
    paid_days_off = serializers.SerializerMethodField()
    unpaid_days_off = serializers.SerializerMethodField()

    def get_paid_day_count(self, instance):
        paid_day_off_count = employee_day_off_list().filter(history = instance, is_paid=True).count()
        return paid_day_off_count

    def get_unpaid_day_count(self, instance):
        unpaid_day_off_count = employee_day_off_list().filter(history = instance, is_paid=False).count()
        return unpaid_day_off_count

    def get_paid_days_off(self,instance):
        qs = list()
        days_off = employee_day_off_list().filter(history = instance, is_paid=True)
        [qs.append(day_off.day_off_date) for day_off in days_off]
        return qs

    def get_unpaid_days_off(self,instance):
        qs = list()
        days_off = employee_day_off_list().filter(history = instance, is_paid=False)
        [qs.append(day_off.day_off_date) for day_off in days_off]
        return qs

    class Meta:
        model = EmployeeDayOffHistory
        fields = '__all__'

class EmployeeDayOffSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = EmployeeDayOff
        fields = '__all__'

class EmployeeDayOffOperationSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, many=True, fields=['id', 'username', 'fullname'])
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='employee', many=True, write_only=True, allow_empty=True
    )

    class Meta:
        model = EmployeeDayOffOperation
        fields = '__all__'