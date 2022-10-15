from django.forms import ValidationError
from rest_framework import serializers
from restAPI.core import DynamicFieldsCategorySerializer

from account.models import EmployeeStatus, User
from company.models import Position
from restAPI.v1.company.serializers import PositionSerializer

from salary.models import (
    AdvancePayment,
    Manager1PrimNew,
    SalaryDeduction,
    Bonus,
    SalaryPunishment,
    SalaryView,
    PaySalary, 
    OfficeLeaderPrim,
    Manager2Prim,
    CreditorPrim,
    GroupLeaderPrimNew
)

from restAPI.v1.account.serializers import EmployeeStatusSerializer, UserSerializer

class AdvancePaymentSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True, fields = ["id", "fullname"])
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.select_related(
                'company', 'office', 'section', 'position', 'team', 'employee_status', 'department'
            ).prefetch_related('user_permissions', 'groups').all(), source='employee', write_only=True
    )

    class Meta:
        model = AdvancePayment
        fields = "__all__"

class SalaryDeductionSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', write_only=True
    )

    class Meta:
        model = SalaryDeduction
        fields = "__all__"

class SalaryPunishmentSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', write_only=True
    )

    class Meta:
        model = SalaryPunishment
        fields = "__all__"
          
        
class BonusSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', write_only=True
    )
  
    class Meta:
        model = Bonus
        fields = "__all__"

class PaySalarySerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = PaySalary
        fields = ('employee', 'amount', 'note', 'salary_date')
        read_only_fields = ('amount',)

class OfficeLeaderPrimSerializer(DynamicFieldsCategorySerializer):
    prim_status = EmployeeStatusSerializer(read_only=True)
    prim_status_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeStatus.objects.all(), source="prim_status", write_only=True
    )

    position = PositionSerializer(read_only=True)
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), source="position", write_only=True
    )

    class Meta:
        model = OfficeLeaderPrim
        fields = "__all__"
    
    def create(self, validated_data):
        prim_status = validated_data.get('prim_status')
        position = validated_data.get('position')
        try:
            prim = OfficeLeaderPrim.objects.filter(prim_status=prim_status, position=position)
            if len(prim)>0:
                raise ValidationError
            return super(OfficeLeaderPrimSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail" : 'Bu status və vəzifəyə uyğun prim artıq əlavə olunub'})


class GroupLeaderPrimNewSerializer(DynamicFieldsCategorySerializer):
    prim_status = EmployeeStatusSerializer(read_only=True)
    prim_status_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeStatus.objects.all(), source="prim_status", write_only=True
    )

    position = PositionSerializer(read_only=True)
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), source="position", write_only=True
    )

    class Meta:
        model = GroupLeaderPrimNew
        fields = "__all__"

    def create(self, validated_data):
        prim_status = validated_data.get('prim_status')
        position = validated_data.get('position')
        try:
            prim = GroupLeaderPrimNew.objects.filter(prim_status=prim_status, position=position)
            if len(prim)>0:
                raise ValidationError
            return super(GroupLeaderPrimNewSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail" : 'Bu status və vəzifəyə uyğun prim artıq əlavə olunub'})


class Manager1PrimNewSerializer(DynamicFieldsCategorySerializer):
    prim_status = EmployeeStatusSerializer(read_only=True)
    prim_status_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeStatus.objects.all(), source="prim_status", write_only=True
    )

    position = PositionSerializer(read_only=True)
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), source="position", write_only=True
    )

    class Meta:
        model = Manager1PrimNew
        fields = "__all__"

    def create(self, validated_data):
        prim_status = validated_data.get('prim_status')
        position = validated_data.get('position')
        try:
            prim = Manager1PrimNew.objects.filter(prim_status=prim_status, position=position)
            if len(prim)>0:
                raise ValidationError
            return super(Manager1PrimNewSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail" : 'Bu status və vəzifəyə uyğun prim artıq əlavə olunub'})

class Manager2PrimSerializer(DynamicFieldsCategorySerializer):
    prim_status = EmployeeStatusSerializer(read_only=True)
    prim_status_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeStatus.objects.all(), source="prim_status", write_only=True
    )

    position = PositionSerializer(read_only=True)
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), source="position", write_only=True
    )

    class Meta:
        model = Manager2Prim
        fields = "__all__"
    
    def create(self, validated_data):
        prim_status = validated_data.get('prim_status')
        position = validated_data.get('position')
        try:
            prim = Manager2Prim.objects.filter(prim_status=prim_status, position=position)
            if len(prim)>0:
                raise ValidationError
            return super(Manager2PrimSerializer, self).create(validated_data)
        except:
            raise ValidationError({"detail" : 'Bu status və vəzifəyə uyğun prim artıq əlavə olunub'})

class CreditorPrimSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = CreditorPrim
        fields = "__all__"

class SalaryViewSerializer(DynamicFieldsCategorySerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', write_only=True
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        month = instance.date.month

        advancepayment = AdvancePayment.objects.filter(employee = instance.employee, date__month=month)
        bonus = Bonus.objects.filter(employee = instance.employee, date__month=month)
        salarydeduction = SalaryDeduction.objects.filter(employee = instance.employee, date__month=month)
        salarypunishment = SalaryPunishment.objects.filter(employee = instance.employee, date__month=month)

        total_advancepayment = 0
        total_bonus = 0
        total_salarydeduction = 0
        total_salarypunishment = 0

        for a in advancepayment:
            total_advancepayment += a.amount

        for b in bonus:
            total_bonus += b.amount

        for k in salarydeduction:
            total_salarydeduction += k.amount

        for p in salarypunishment:
            total_salarypunishment += p.amount


        representation['advancepayment'] = total_advancepayment
        representation['bonus'] = total_bonus
        representation['salarydeduction'] = total_salarydeduction
        representation['salarypunishment'] = total_salarypunishment

        return representation
    
    class Meta:
        model = SalaryView
        fields = '__all__'
        read_only_fields = ('advancepayment', 'bonus', 'salarydeduction', 'salarypunishment')