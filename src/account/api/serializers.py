from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Permission, Group
from core.utils.base_serializer import DynamicFieldsCategorySerializer

from account.models import (
    User,
    Customer,
    Region,
    EmployeeStatus,
    EmployeeActivity,
)
from account.api.selectors import user_list, employee_status_list, region_list

from company.api.selectors import company_list, office_list, section_list, department_list, position_list
from company.api.serializers import (
    CompanySerializer,
    OfficeSerializer,
    PositionSerializer,
    DepartmentSerializer,
    SectionSerializer
)
from contract.api.selectors import contract_list
from contract import REMOVED, CONTINUING

from services.api.selectors import service_list

from salary.models import Commission


class PermissionSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = Permission
        fields = "__all__"

class GroupSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = Group
        fields = "__all__"

class EmployeeStatusSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = EmployeeStatus
        fields = "__all__"


class RegionSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = Region
        fields = "__all__"


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password reset endpoint.
    """
    username = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class RegisterSerializer(DynamicFieldsCategorySerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    register_type = serializers.CharField(required=True)
    salary_style = serializers.CharField(required=True)
    photo_ID = serializers.ImageField(required=True)
    electronic_signature = serializers.ImageField(required=True)
    phone_number_1 = serializers.CharField(required=True)
    position = serializers.PrimaryKeyRelatedField(
        queryset=position_list(), write_only=True, required=True  
    )
    fin_code = serializers.CharField(required=True)

    def validate_fin_code(self,value):
        if user_list().filter(fin_code=value).exists():
            raise serializers.ValidationError({'unique': 'Bu fin kod ilə işçi artıq əlavə edilib'})
        else:
            return value

    class Meta:
        model = User
        fields = (
            'id', 'fullname', 'phone_number_1', 'phone_number_2', 'region','address',
            'email','company', 'office', 'department', 'section','supervisor','position', 
            'photo_ID', 'back_photo_of_ID', 'driving_license_photo', 
            'employee_status','commission','salary_style', 'salary', 'note', 
            'electronic_signature','profile_image','register_type', 'user_permissions',
            'groups', 'password', 'app_permission', 'fin_code'
        )


class UserSerializer(DynamicFieldsCategorySerializer):
    class CommissionSerializer(DynamicFieldsCategorySerializer):
        """
        Komissiya serializer-ın burada inline yazılmasına səbəb, bu formada yazmadıqda
        circular error verməsidir.
        """
        class Meta:
            model = Commission
            fields = (
                'id',
                'commission_name',
            )
    class SupervizorSerializer(DynamicFieldsCategorySerializer):
        class Meta:
            model = User
            fields = (
                'id',
                'username',
                'fullname'
            )

    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    department = DepartmentSerializer(read_only=True, fields=['id', 'name'])
    section = SectionSerializer(read_only=True, fields=['id', 'name'])
    office = OfficeSerializer(read_only=True, fields=['id', 'name'])
    position = PositionSerializer(read_only=True, fields=['id', 'name'])
    employee_status = EmployeeStatusSerializer(read_only=True, fields=['id', 'status_name'])
    dismissal_date = serializers.DateField(read_only=True)
    commission = CommissionSerializer(read_only=True, fields=['id', 'commission_name'])
    region = RegionSerializer(read_only=True, fields=['id', 'region_name'])
    supervisor = SupervizorSerializer(read_only=True, fields=['id', 'username', 'fullname'])
    
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=company_list(), source='company', write_only=True, allow_null=True
    )
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=department_list(), source='department', write_only=True, allow_null=True
    )
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=section_list(), source='section', write_only=True, allow_null=True
    )
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=office_list(), source='office', write_only=True, allow_null=True
    )

    position_id = serializers.PrimaryKeyRelatedField(
        queryset=position_list(), source='position', write_only=True, allow_null=True
    )

    employee_status_id = serializers.PrimaryKeyRelatedField(
        queryset=employee_status_list(), source='employee_status', write_only=True, allow_null=True
    )

    commission_id = serializers.PrimaryKeyRelatedField(
        queryset=Commission.objects.prefetch_related('installment', 'for_sale_range').all(), source='commission', write_only=True, allow_null=True
    )

    region_id = serializers.PrimaryKeyRelatedField(
        queryset=region_list(), source='region', write_only=True, allow_null=True
    )

    supervisor_id = serializers.PrimaryKeyRelatedField(
        queryset=user_list(), source='supervisor', write_only=True, allow_null=True
    )

    class Meta:
        model = User
        exclude = ('last_login', 'is_staff', 'password')


class CustomerSerializer(DynamicFieldsCategorySerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=region_list(), source="region", write_only=True
    )

    is_active = serializers.BooleanField(read_only=True)
    
    contract_count = serializers.SerializerMethodField()
    service_count = serializers.SerializerMethodField()
    
    def get_contract_count(self, instance):
        contract_count = contract_list().filter(customer=instance).count()
        return contract_count

    def get_service_count(self, instance):
        service_count = service_list().filter(customer=instance).count()
        return service_count

    class Meta:
        model = Customer
        fields = "__all__"

class EmployeeActivitySerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = EmployeeActivity
        fields = "__all__"