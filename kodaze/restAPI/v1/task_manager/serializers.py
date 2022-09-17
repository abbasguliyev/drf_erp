from rest_framework import serializers
from company.models import Vezifeler
from task_manager.models import TaskManager, UserTaskRequest
from restAPI.v1.company.serializers import VezifelerSerializer
from restAPI.v1.account.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class PositionForTaskManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vezifeler
        fields = ['id', 'vezife_adi']

class UserForTaskManagerSerializer(serializers.ModelSerializer):
    vezife = PositionForTaskManagerSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'asa', 'tel1', 'vezife']

class TaskManagerSerializer(serializers.ModelSerializer):
    position = PositionForTaskManagerSerializer(read_only=True)
    employee = UserForTaskManagerSerializer(read_only=True)

    # position_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Vezifeler.objects.all(), source='position', write_only=True, required=False, allow_null=True
    # )
    # employee_id = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(), source='employee', write_only=True, required=False, allow_null=True
    # )

    users = serializers.CharField(write_only=True,required=False, allow_null=True)
    positions = serializers.CharField(write_only=True,required=False, allow_null=True)

    class Meta:
        model = TaskManager
        fields = (
            'id',
            'title', 
            'description', 
            'created_date', 
            'end_date', 
            'position', 
            'employee', 
            'type',
            'status',
            'users',
            'positions'
        )


class UserTaskRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTaskRequest
        fields = "__all__"
