from rest_framework import serializers
from company.models import Vezifeler
from task_manager.models import Advertisement, TaskManager, UserTaskRequest
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
    creator = UserForTaskManagerSerializer(read_only=True)
    position = PositionForTaskManagerSerializer(read_only=True)
    employee = UserForTaskManagerSerializer(read_only=True)

    users = serializers.CharField(write_only=True,required=False, allow_null=True)
    positions = serializers.CharField(write_only=True,required=False, allow_null=True)

    class Meta:
        model = TaskManager
        fields = (
            'id',
            'title', 
            'body', 
            'creator', 
            'created_date', 
            'end_date', 
            'position', 
            'employee', 
            'status',
            'users',
            'positions'
        )


class UserTaskRequestSerializer(serializers.ModelSerializer):
    creator = UserForTaskManagerSerializer(read_only=True)

    class Meta:
        model = UserTaskRequest
        fields = "__all__"

class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserForTaskManagerSerializer(read_only=True)

    position = PositionForTaskManagerSerializer(read_only=True)
    positions = serializers.CharField(write_only=True,required=False, allow_null=True)

    class Meta:
        model = Advertisement
        fields = (
            'id',
            'title', 
            'creator', 
            'body', 
            'created_date', 
            'position', 
            'positions'
        )