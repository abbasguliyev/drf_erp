from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import django
from restAPI.core import DynamicFieldsCategorySerializer
from account.models import (
    CustomerNote,
    User,
    Customer,
    Region,
    EmployeeStatus
)
from restAPI.v1.company.serializers import (
    CompanySerializer,
    HoldingSerializer,
    OfficeSerializer,
    SectionSerializer,
    TeamSerializer,
    PositionSerializer,
    DepartmentSerializer
)

from company.models import (
    Company,
    Holding,
    Office,
    Team,
    Section,
    PermissionForPosition,
    Position,
    Department
)

from django.contrib.auth.models import Permission, Group


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
    contract_type = serializers.CharField(required=True)
    salary_style = serializers.CharField(required=True)
    photo_ID = serializers.ImageField(required=True)
    phone_number_1 = serializers.CharField(required=True)
    start_date_of_work = serializers.DateField(format="%d-%m-%Y", required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'id', 
            'fullname', 
            'start_date_of_work',
            'dismissal_date',
            'phone_number_1', 
            'phone_number_2', 
            'photo_ID', 
            'back_photo_of_ID', 
            'driving_license_photo', 
            'company', 
            'department',
            'office', 
            'section', 
            'position', 
            'team', 
            'employee_status',
            'user_permissions', 
            'groups', 
            'profile_image',
            'contract_type', 
            'salary_style', 
            'salary', 
            'supervisor', 
            'note', 
            'password', 
        )


class UserSerializer(DynamicFieldsCategorySerializer):
    holding = HoldingSerializer(read_only=True, fields=['id', 'name'])
    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    department = DepartmentSerializer(read_only=True, fields=['id', 'name'])
    office = OfficeSerializer(read_only=True, fields=['id', 'name'])
    section = SectionSerializer(read_only=True, fields=['id', 'name'])
    position = PositionSerializer(read_only=True, fields=['id', 'name'])
    team = TeamSerializer(read_only=True, fields=['id', 'name'])
    employee_status = EmployeeStatusSerializer(read_only=True, fields=['id', 'status_name'])
    user_permissions = PermissionSerializer(read_only=True, many=True, fields=['id', 'name'])
    groups = GroupSerializer(read_only=True, many=True, fields=['id', 'name'])
    dismissal_date = serializers.DateField(read_only=True)

    holding_id = serializers.PrimaryKeyRelatedField(
        queryset=Holding.objects.all(), source='holding', write_only=True, allow_null=True
    )
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.select_related('holding').all(), source='company', write_only=True,
    )
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.select_related('holding').all(), source='department', write_only=True
    )
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.select_related('company').all(), source='office', write_only=True
    )
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.select_related('office').all(), source='section',
        write_only=True, required=False, allow_null=True
    )

    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.select_related('company').all(), source='position', write_only=True,
    )

    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='team', write_only=True,
    )

    employee_status_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeStatus.objects.all(), source='employee_status', write_only=True,
    )

    user_permissions_id = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), source='user_permissions', write_only=True, many=True
    )

    groups_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), source='groups', write_only=True, many=True
    )

    class Meta:
        model = User
        exclude = ('password',)

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
        queryset=Region.objects.all(), source="region", write_only=True
    )

    is_active = serializers.BooleanField(read_only=True)
    class Meta:
        model = Customer
        fields = "__all__"
        


class CustomerNoteSerializer(DynamicFieldsCategorySerializer):
    customer = CustomerSerializer(read_only=True, fields=['id', 'fullname'])

    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.select_related('region').all(), source='customer', write_only=True
    )

    class Meta:
        model = CustomerNote
        fields = "__all__"