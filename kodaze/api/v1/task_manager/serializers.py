from rest_framework import serializers
from api.core import DynamicFieldsCategorySerializer

from company.models import Position
from task_manager.models import Advertisement, TaskManager, UserTaskRequest
from api.v1.company.serializers import PositionSerializer
from api.v1.account.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class PositionForTaskManagerSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = Position
        fields = ['id', 'name']


class UserForTaskManagerSerializer(DynamicFieldsCategorySerializer):
    position = PositionForTaskManagerSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'fullname', 'phone_number_1', 'position']


class TaskManagerSerializer(DynamicFieldsCategorySerializer):
    creator = UserForTaskManagerSerializer(read_only=True)
    position = PositionForTaskManagerSerializer(read_only=True)
    employee = UserForTaskManagerSerializer(read_only=True)
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.select_related('company').all(), source='position', write_only=True, allow_null=True
    )
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.select_related(
            'company', 'office', 'section', 'position', 'team', 'employee_status', 'department'
        ).prefetch_related('user_permissions', 'groups').all(), source='employee', write_only=True, allow_null=True
    )
    users = serializers.CharField(write_only=True, required=False, allow_null=True)
    positions = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = TaskManager
        fields = (
            'id',
            'title',
            'body',
            'creator',
            'created_date',
            'end_date',
            'old_date',
            'position',
            'employee',
            'position_id',
            'employee_id',
            'status',
            'users',
            'positions',

        )


class UserTaskRequestSerializer(DynamicFieldsCategorySerializer):
    creator = UserForTaskManagerSerializer(read_only=True)

    class Meta:
        model = UserTaskRequest
        fields = "__all__"


class AdvertisementSerializer(DynamicFieldsCategorySerializer):
    creator = UserForTaskManagerSerializer(read_only=True)

    position = PositionForTaskManagerSerializer(read_only=True, many=True)
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.select_related('company').all(), source='position', write_only=True, many=True
    )

    class Meta:
        model = Advertisement
        fields = (
            'id',
            'title',
            'creator',
            'body',
            'created_date',
            'position',
            'position_id'
        )
