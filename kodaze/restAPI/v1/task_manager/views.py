from datetime import datetime
import traceback
import django
from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from restAPI.v1.task_manager.serializers import TaskManagerSerializer, UserTaskRequestSerializer
from task_manager.models import TaskManager, UserTaskRequest

from restAPI.v1.task_manager.filters import TaskManagerFilter
from . import permissions
from restAPI.v1.utils.permission_utils import IsAdminUserOrReadOnly
from django.contrib.auth import get_user_model
User = get_user_model()


class TaskManagerListCreateAPIView(generics.ListCreateAPIView):
    queryset = TaskManager.objects.all()
    serializer_class = TaskManagerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskManagerFilter
    permission_classes = [permissions.TaskManagerPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            position = serializer.validated_data.get("position")
            end_date = serializer.validated_data.get('end_date')
            print(f"{end_date=}")
            if end_date == None:
                end_date = datetime.today()
            if position is not None:
                print(f"{position=}")
                users = User.objects.filter(vezife=position)
                print(f"{users=}")
                for user in users:
                    task_manager = TaskManager.objects.create(
                        title = serializer.validated_data.get('title'),
                        description = serializer.validated_data.get('description'),
                        document = serializer.validated_data.get('document'),
                        end_date = end_date,
                        position = position,
                        employee = user,
                        type = serializer.validated_data.get('type'),
                    )
                    task_manager.save()
            else:
                serializer.save()
            return Response({"detail": "Tapşırıq əlavə edildi"}, status=status.HTTP_201_CREATED)
        else:
            traceback.print_exc

class TaskManagerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskManager.objects.all()
    serializer_class = TaskManagerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskManagerFilter
    permission_classes = [permissions.TaskManagerPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail": "Məlumatlar yeniləndi"})


class UserTaskRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserTaskRequest.objects.all()
    serializer_class = UserTaskRequestSerializer
    filter_backends = [DjangoFilterBackend]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Tapşırıq əlavə edildi"}, status=status.HTTP_201_CREATED, headers=headers)


class UserTaskRequestDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserTaskRequest.objects.all()
    serializer_class = UserTaskRequestSerializer
    filter_backends = [DjangoFilterBackend]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail": "Məlumatlar yeniləndi"})
