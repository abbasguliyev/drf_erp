from django.forms import ValidationError
from rest_framework import serializers
from account.models import EmployeeStatus, User
from company.models import Position
from restAPI.v1.company.serializers import PositionSerializer

from salary.models import (
    AdvancePayment,
    Manager1PrimNew,
    SalaryDeduction,
    Bonus,
    SalaryView,
    PaySalary, 
    OfficeLeaderPrim,
    Manager2Prim,
    CreditorPrim,
    GroupLeaderPrimNew
)

from restAPI.v1.account.serializers import EmployeeStatusSerializer, UserSerializer

class AdvancePaymentSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True, many=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', many=True, write_only=True
    )

    class Meta:
        model = AdvancePayment
        fields = "__all__"

class SalaryDeductionSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', write_only=True
    )

    class Meta:
        model = SalaryDeduction
        fields = "__all__"
        
        
class BonusSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', write_only=True
    )
  
    class Meta:
        model = Bonus
        fields = "__all__"

class PaySalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaySalary
        fields = ('employee', 'amount', 'note', 'installment')
        read_only_fields = ('amount',)

class OfficeLeaderPrimSerializer(serializers.ModelSerializer):
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


class GroupLeaderPrimNewSerializer(serializers.ModelSerializer):
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


class Manager1PrimNewSerializer(serializers.ModelSerializer):
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

class Manager2PrimSerializer(serializers.ModelSerializer):
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

class CreditorPrimSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditorPrim
        fields = "__all__"

class SalaryViewSerializer(serializers.ModelSerializer):
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

        umumi_advancepayment = 0
        umumi_bonus = 0
        umumi_salarydeduction = 0

        for a in advancepayment:
            umumi_advancepayment += a.amount

        for b in bonus:
            umumi_bonus += b.amount

        for k in salarydeduction:
            umumi_salarydeduction += k.amount

        representation['advancepayment'] = umumi_advancepayment
        representation['bonus'] = umumi_bonus
        representation['salarydeduction'] = umumi_salarydeduction

        return representation
    
    class Meta:
        model = SalaryView
        fields = '__all__'
        read_only_fields = ('advancepayment', 'bonus', 'salarydeduction')