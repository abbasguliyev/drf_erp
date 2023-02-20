from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.utils.base_serializer import DynamicFieldsCategorySerializer

from account.models import (
    User
)

from company.models import (
    Department,
    Holding,
    Company,
    Office,
    Team,
    Section,
    PermissionForPosition,
    Position,
    AppLogo
)
from company.api.selectors import company_list, office_list, department_list, section_list, team_list, position_list
from django.contrib.auth.models import Group
from account.api.selectors import user_list


class PositionUserSerializer(DynamicFieldsCategorySerializer):
    """
    Bu Seriazlier UserOperationSeriazlier-de positioni istifade etmek ucun istifade olunur
    """
    class Meta:
        model = Position
        fields = ['name']


class UserOperationSerializer(DynamicFieldsCategorySerializer):
    """
    Bu Seriazlier Kassa Əməliyyatlarında User-in(transferi eden işçinin) melumatlarini gostermek ucun istifade olur
    """
    position = PositionUserSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['fullname', 'position']



class HoldingSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = Holding
        fields = "__all__"

class CompanySerializer(DynamicFieldsCategorySerializer):
    employee_count = serializers.SerializerMethodField('employee_count_fn')
    office_count = serializers.SerializerMethodField('office_count_fn')

    def employee_count_fn(self, instance):
        employees = user_list().filter(company=instance, is_active=True).count()
        return employees

    def office_count_fn(self, instance):
        offices = office_list().filter(company=instance, is_active=True).count()
        return offices

    class Meta:
        model = Company
        fields = ('id', 'name', 'address', 'phone', 'email', 'web_site', 'is_active', 'employee_count', 'office_count')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name).upper()
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.web_site = validated_data.get('web_site', instance.web_site)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class DepartmentSerializer(DynamicFieldsCategorySerializer):
    employee_count = serializers.SerializerMethodField('employee_count_fn')

    def employee_count_fn(self, instance):
        employees = user_list().filter(department= instance, is_active= True).count()
        return employees

    class Meta:
        model = Department
        fields = ('id', 'name', 'is_active', 'employee_count')
    

class OfficeSerializer(DynamicFieldsCategorySerializer):
    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=company_list(), source='company', write_only=True
    )

    employee_count = serializers.SerializerMethodField('employee_count_fn')

    def employee_count_fn(self, instance):
        employees = user_list().filter(office= instance, is_active= True).count()
        return employees


    class Meta:
        model = Office
        fields = ('id', 'name', 'company', 'company_id', 'is_active', 'employee_count')


class SectionSerializer(DynamicFieldsCategorySerializer):
    
    class Meta:
        model = Section
        fields = ('id', 'name', 'is_active',)
    

class TeamSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = Team
        fields = "__all__"

    def create(self, validated_data):
        name = validated_data.get('name')
        validated_data['name'] = name.upper()
        try:
            k = Team.objects.filter(
                name=name.upper(), is_active=True)
            if len(k) > 0:
                raise ValidationError
            return super(TeamSerializer, self).create(validated_data)
        except:
            raise ValidationError(
                {"detail": 'Bu ad ilə team artıq əlavə olunub'})

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name).upper()
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class PositionSerializer(DynamicFieldsCategorySerializer):
    employees_count = serializers.SerializerMethodField("employees_count_fn")

    def employees_count_fn(self, instance):
        employees = user_list().filter(position= instance, is_active= True).count()
        return employees

    class Meta:
        model = Position
        fields = ('id', 'name', 'employees_count', 'is_active')

class PermissionForPositionSerializer(DynamicFieldsCategorySerializer):
    position = PositionSerializer(read_only=True, fields=['id', 'name'])
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=position_list(), source='position', write_only=True
    )

    permission_group = serializers.StringRelatedField(read_only=True)
    permission_group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), source='permission_group', write_only=True, allow_null=True
    )

    class Meta:
        model = PermissionForPosition
        fields = '__all__'


class AppLogoSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = AppLogo
        fields = '__all__'
