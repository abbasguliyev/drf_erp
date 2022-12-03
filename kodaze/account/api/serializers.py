from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from django.db.models import Sum, Q
from django.db.models import CharField, FloatField, DateField, IntegerField, Value

from core.utils.base_serializer import DynamicFieldsCategorySerializer
from account.models import (
    User,
    Customer,
    Region,
    EmployeeStatus
)
from company.api.serializers import (
    CompanySerializer,
    OfficeSerializer,
    PositionSerializer,
    DepartmentSerializer
)

from company.models import (
    Company,
    Office,
    Position,
    Department
)

from contract.models import DemoSales

from salary.models import SalaryView
from salary.api.selectors import salary_view_list
from account.api.selectors import user_list

from django.contrib.auth.models import Permission, Group
from account.api.selectors import employee_status_list, region_list
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
        queryset=Position.objects.all(), write_only=True, required=True  
    )

    class Meta:
        model = User
        fields = (
            'id', 'fullname', 'phone_number_1', 'phone_number_2', 'region','address',
            'email','company', 'office', 'department','supervisor','position', 
            'photo_ID', 'back_photo_of_ID', 'driving_license_photo', 
            'employee_status','commission','salary_style', 'salary', 'note', 
            'electronic_signature','profile_image','register_type', 'user_permissions',
            'groups', 'password', 
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
    office = OfficeSerializer(read_only=True, fields=['id', 'name'])
    position = PositionSerializer(read_only=True, fields=['id', 'name'])
    employee_status = EmployeeStatusSerializer(read_only=True, fields=['id', 'status_name'])
    user_permissions = PermissionSerializer(read_only=True, many=True, fields=['id', 'name'])
    groups = GroupSerializer(read_only=True, many=True, fields=['id', 'name'])
    dismissal_date = serializers.DateField(read_only=True)
    commission = CommissionSerializer(read_only=True, fields=['id', 'commission_name'])
    region = RegionSerializer(read_only=True, fields=['id', 'region_name'])
    supervisor = SupervizorSerializer(read_only=True, fields=['id', 'username', 'fullname'])

    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True,
    )
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source='department', write_only=True
    )
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.select_related('company').all(), source='office', write_only=True
    )

    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), source='position', write_only=True,
    )

    employee_status_id = serializers.PrimaryKeyRelatedField(
        queryset=employee_status_list(), source='employee_status', write_only=True,
    )

    user_permissions_id = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), source='user_permissions', write_only=True, many=True
    )

    groups_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), source='groups', write_only=True, many=True
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

    def update(self, instance, validated_data):
        user = instance
        user_permissions = validated_data.get('user_permissions')
        if user_permissions is not None:
            for user_permission in user_permissions:
                user.user_permissions.add(user_permission)

        instance.save()
        return super().update(instance, validated_data)


class CustomerSerializer(DynamicFieldsCategorySerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=region_list(), source="region", write_only=True
    )

    is_active = serializers.BooleanField(read_only=True)
    class Meta:
        model = Customer
        fields = "__all__"