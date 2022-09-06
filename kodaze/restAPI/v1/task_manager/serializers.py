from rest_framework import serializers
from company.models import Vezifeler
from task_manager.models import TaskManager, UserTaskRequest
from restAPI.v1.company.serializers import VezifelerSerializer
from restAPI.v1.account.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskManagerSerializer(serializers.ModelSerializer):
    position = VezifelerSerializer(read_only=True)
    employee = UserSerializer(read_only=True)

    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Vezifeler.objects.all(), source='position', write_only=True, required=False, allow_null=True
    )
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='employee', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = TaskManager
        fields = "__all__"


class UserTaskRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTaskRequest
        fields = "__all__"
