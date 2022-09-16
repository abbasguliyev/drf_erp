from datetime import datetime
import traceback
import django
from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from restAPI.v1.task_manager.serializers import TaskManagerSerializer, UserTaskRequestSerializer
from task_manager.models import TaskManager, UserTaskRequest
from company.models import Vezifeler
from restAPI.v1.task_manager.filters import TaskManagerFilter, UserTaskRequestFilter
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

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        toplam_tapsiriq_sayi = 0
        tamamlandi = 0
        icra_edilir = 0
        gecikir = 0

        page = self.paginate_queryset(queryset)
        if page == None:
            page = queryset
        for q in page:
            toplam = TaskManager.objects.filter(pk = q.id).count()
            tamamlanan = TaskManager.objects.filter(pk = q.id, status="Tamamlandı").count()
            icra_edilen = TaskManager.objects.filter(pk = q.id, status="İcra edilir").count()
            geciken = TaskManager.objects.filter(pk = q.id, status="Gecikir").count()

            toplam_tapsiriq_sayi += toplam
            tamamlandi += tamamlanan
            icra_edilir += icra_edilen
            gecikir += geciken
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # serializer.data
            return self.get_paginated_response([{
                    'toplam_tapsiriq_sayi':toplam_tapsiriq_sayi,
                    'tamamlandi':tamamlandi,
                    'icra_edilir':icra_edilir,
                    'gecikir':gecikir,
                    'date':serializer.data
            }])

        serializer = self.get_serializer(queryset, many=True)
        return Response([{
                    'toplam_tapsiriq_sayi':toplam_tapsiriq_sayi,
                    'tamamlandi':tamamlandi,
                    'icra_edilir':icra_edilir,
                    'gecikir':gecikir,
                    'date':serializer.data
            }])
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            position_str = serializer.validated_data.get("positions")
            if position_str is not None:
                position_list = position_str.split(',')
            else:
                position_list = None
            user_str = serializer.validated_data.get("users")
            if user_str is not None:
                user_list = user_str.split(',')
            else:
                user_list = None
            created_date = serializer.validated_data.get('created_date')
            if created_date == None:
                created_date = datetime.today()
            end_date = serializer.validated_data.get('end_date')
            if end_date == None:
                end_date = None

            if position_list is not None:
                for position_id in position_list:
                    position = Vezifeler.objects.get(pk=position_id)
                    users = User.objects.filter(vezife=position)
                    for user in users:
                        task_manager = TaskManager.objects.create(
                            title = serializer.validated_data.get('title'),
                            description = serializer.validated_data.get('description'),
                            created_date = created_date,
                            end_date = end_date,
                            position = position,
                            employee = user,
                            type = serializer.validated_data.get('type'),
                        )
                        task_manager.save()
            if user_list is not None:
                for user_id in user_list:
                    user = User.objects.get(pk=user_id)
                    task_manager = TaskManager.objects.create(
                        title = serializer.validated_data.get('title'),
                        description = serializer.validated_data.get('description'),
                        created_date = created_date,
                        end_date = end_date,
                        employee = user,
                        type = serializer.validated_data.get('type'),
                    )
                    task_manager.save()
            if user_list == None and position_list == None:
                return Response({'detail' : "İşçi və ya vəzifədən biri mütləq seçilməlidir"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Tapşırıq əlavə edildi"}, status=status.HTTP_201_CREATED)
        else:
            traceback.print_exc
            return Response({'detail' : "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

class TaskManagerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskManager.objects.all()
    serializer_class = TaskManagerSerializer
    filter_backends = [DjangoFilterBackend]
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
    filterset_class = UserTaskRequestFilter


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Sorğu əlavə edildi"}, status=status.HTTP_201_CREATED, headers=headers)


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
