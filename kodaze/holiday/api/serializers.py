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

from company.models import Company, Office

from account.api.serializers import UserSerializer
from account.api.selectors import user_list

from company.api.serializers import (
    CompanySerializer,
    OfficeSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeWorkingDaySerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = EmployeeWorkingDay
        fields = '__all__'

class EmployeeHolidayHistorySerializer(DynamicFieldsCategorySerializer):
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

    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True,
    )

    office = OfficeSerializer(read_only=True, fields=['id', 'name'])
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.select_related('company').all(), source='office', write_only=True
    )

    class Meta:
        model = HolidayOperation
        fields = '__all__'

class EmployeeDayOffHistorySerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = EmployeeDayOffHistory
        fields = '__all__'

class EmployeeDayOffSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = EmployeeDayOff
        fields = '__all__'

class EmployeeDayOffOperationSerializer(DynamicFieldsCategorySerializer):
    person_on_duty = UserSerializer(read_only=True, many=True, fields=['id', 'username', 'fullname'])
    person_on_duty_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='person_on_duty', many=True, write_only=True, allow_empty=True
    )

    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True,
    )

    office = OfficeSerializer(read_only=True, fields=['id', 'name'])
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.select_related('company').all(), source='office', write_only=True
    )

    class Meta:
        model = EmployeeDayOffOperation
        fields = '__all__'