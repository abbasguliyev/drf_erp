from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from restAPI.core import DynamicFieldsCategorySerializer

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
from django.contrib.auth.models import Group

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
    class Meta:
        model = Company
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        offices = Office.objects.filter(company=instance, is_active=True).count()
        employees = User.objects.filter(company=instance, is_active=True).count()
        representation['office_count'] = offices
        representation['employee_count'] = employees

        return representation

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name).upper()
        instance.holding = validated_data.get('holding', instance.holding)
        instance.holding = validated_data.get('address', instance.address)
        instance.holding = validated_data.get('phone', instance.phone)
        instance.holding = validated_data.get('email', instance.email)
        instance.holding = validated_data.get('web_site', instance.web_site)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class DepartmentSerializer(DynamicFieldsCategorySerializer):
    holding = HoldingSerializer(read_only=True)
    holding_id = serializers.PrimaryKeyRelatedField(
        queryset=Holding.objects.all(), source='holding', write_only=True
    )

    class Meta:
        model = Department
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        employees = User.objects.filter(department=instance, is_active=True).count()
        representation['employee_count'] = employees

        return representation

    def create(self, validated_data):
        name = validated_data.get('name')
        validated_data['name'] = name.upper()
        holding = validated_data['holding']
        try:
            departmentt = Department.objects.filter(
                name=name.upper(), holding=holding)
            if len(departmentt) > 0:
                raise ValidationError
            return super(DepartmentSerializer, self).create(validated_data)
        except:
            raise ValidationError(
                {"detail": 'Bu ad ilə departament artıq əlavə olunub'})

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name', instance.name).upper()
        instance.holding = validated_data.get('holding', instance.holding)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()
        return instance


class OfficeSerializer(DynamicFieldsCategorySerializer):
    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.select_related('holding').all(), source='company', write_only=True
    )

    class Meta:
        model = Office
        fields = "__all__"

    def create(self, validated_data):
        name = validated_data.get('name')
        validated_data['name'] = name.upper()
        company = validated_data['company']
        try:
            offices = Office.objects.filter(
                name=name.upper(), company=company)
            if len(offices) > 0:
                raise ValidationError
            return super(OfficeSerializer, self).create(validated_data)
        except:
            raise ValidationError(
                {"detail": 'Bu ad ilə office artıq əlavə olunub'})

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name', instance.name).upper()
        instance.company = validated_data.get('company', instance.company)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()
        return instance


class SectionSerializer(DynamicFieldsCategorySerializer):
    office = OfficeSerializer(read_only=True, fields=['id', 'name'])
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.select_related('company').all(), source='office', write_only=True
    )

    class Meta:
        model = Section
        fields = "__all__"

    def create(self, validated_data):
        name = validated_data.get('name')
        validated_data['name'] = name.upper()
        office = validated_data['office']
        try:
            section_qs = Section.objects.filter(
                name=name.upper(), office=office)
            if len(section_qs) > 0:
                raise ValidationError
            return super(SectionSerializer, self).create(validated_data)
        except:
            raise ValidationError(
                {"detail": 'Bu ad ilə şöbə artıq əlavə olunub'})

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name).upper()
        instance.office = validated_data.get('office', instance.office)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

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
    company = CompanySerializer(read_only=True, fields=['id', 'name'])
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )

    class Meta:
        model = Position
        fields = "__all__"

    def create(self, validated_data):
        name = validated_data.get('name')
        validated_data['name'] = name.upper()
        return super(PositionSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name).upper()
        instance.company = validated_data.get('company', instance.company)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class PermissionForPositionSerializer(DynamicFieldsCategorySerializer):
    position = PositionSerializer(read_only=True, fields=['id', 'name'])
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), source='position', write_only=True
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
