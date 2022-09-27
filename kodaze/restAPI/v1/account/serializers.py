from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import django
from account.models import (
    CustomerNote,
    User,
    Customer,
    Region,
    EmployeeStatus
)
from restAPI.v1.company.serializers import (
    CompanySerializer,
    OfficeSerializer,
    SectionSerializer,
    TeamSerializer,
    PositionSerializer
)

from company.models import (
    Company,
    Office,
    Team,
    Section,
    PermissionForPosition,
    Position
)

from django.contrib.auth.models import Permission, Group
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class GroupReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class EmployeeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeStatus
        fields = "__all__"

    def create(self, validated_data):
        status_name = validated_data.get('status_name')
        validated_data['status_name'] = status_name.upper()
        return super(EmployeeStatusSerializer, self).create(validated_data)


class RegionSerializer(serializers.ModelSerializer):
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


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

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
            'password2',
        )

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        if data['phone_number_1'] == None:
            raise serializers.ValidationError(
                {"phone_number_1": "Ən az 1 telefon nömrəsi daxil edin"})
        return data

    def create(self, validated_data):
        last_user_id = User.objects.all().values_list('id', flat=True).last()
        username=f"user-{last_user_id+1}"
        user = User.objects.create(
            username=username,
            fullname=validated_data['fullname'], 
            phone_number_1=validated_data['phone_number_1'],
            photo_ID=validated_data['photo_ID'],
            salary_style=validated_data['salary_style'],
            contract_type=validated_data['contract_type'],
        )
        user.set_password(validated_data['password'])
        

        try:
            user.back_photo_of_ID = validated_data['back_photo_of_ID']
        except:
            user.back_photo_of_ID = None
        try:
            user.profile_image = validated_data['profile_image']
        except:
            user.profile_image = None

        try:
            user.driving_license_photo = validated_data['driving_license_photo']
        except:
            user.driving_license_photo = None

        try:
            user.start_date_of_work = validated_data['start_date_of_work']
        except:
            user.start_date_of_work = django.utils.timezone.now()
        
        try:
            user.dismissal_date = validated_data['dismissal_date']
        except:
            user.dismissal_date = None
        try:
            user.salary = validated_data['salary']
        except:
            user.salary = 0

        try:
            user.department = validated_data['department']
        except:
            user.department = None
        
        try:
            user.company=validated_data['company']
        except:
            user.company = None
        
        try:
            user.office=validated_data['office']
        except:
            user.office = None

        try:
            user.section = validated_data['section']
        except:
            user.section = None
        try:
            user.position=validated_data['position']
            permission_for_positions = PermissionForPosition.objects.filter(position=user.position)
            if permission_for_positions is not None:
                for vp in permission_for_positions:
                    permission_group = vp.permission_group
                    user.groups.add(permission_group)
        except:
            user.position = None
            
        try:
            user.phone_number_2 = validated_data['phone_number_2']
        except:
            user.phone_number_2 = None

        try:
            user.team = validated_data['team']
        except:
            user.team = None
        
        try:
            user.employee_status=validated_data['employee_status']
        except:
            user.employee_status = None
        try:
            user.supervisor=validated_data['supervisor']
        except:
            user.supervisor = None

        try:
            user.note=validated_data['note']
        except:
            user.note = None

        user_permissions = validated_data['user_permissions']
        for user_permission in user_permissions:
            user.user_permissions.add(user_permission)

        # permission_for_positions = get_object_or_404(PermissionForPosition, )
        groups = validated_data['groups']
        for group in groups:
            user.groups.add(group)

        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    office = OfficeSerializer(read_only=True)
    section = SectionSerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.select_related('holding').all(), source='company', write_only=True,
    )
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.select_related('company').all(), source='office', write_only=True
    )
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.select_related('office').all(), source='section',
        write_only=True, required=False, allow_null=True
    )

    position = PositionSerializer(read_only=True)
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.select_related('section', 'company').all(), source='position', write_only=True,
    )

    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='team', write_only=True,
    )

    employee_status = EmployeeStatusSerializer(read_only=True)
    employee_status_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeStatus.objects.all(), source='employee_status', write_only=True,
    )

    user_permissions = PermissionSerializer(read_only=True, many=True)
    user_permissions_id = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), source='user_permissions', write_only=True, many=True
    )

    dismissal_date = serializers.DateField(read_only=True)

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


class CustomerSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), source="region", write_only=True
    )

    class Meta:
        model = Customer
        fields = "__all__"


class CustomerNoteSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True
    )

    class Meta:
        model = CustomerNote
        fields = "__all__"