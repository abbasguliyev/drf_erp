from datetime import datetime
import traceback
from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from restAPI.v1.task_manager.serializers import TaskManagerSerializer, UserTaskRequestSerializer, AdvertisementSerializer
from task_manager.models import TaskManager, UserTaskRequest, Advertisement
from company.models import Position
from restAPI.v1.task_manager.filters import TaskManagerFilter, UserTaskRequestFilter, AdvertisementFilter
from . import permissions

from django.contrib.auth import get_user_model
from django.db.models import Count



User = get_user_model()


class TaskManagerListCreateAPIView(generics.ListCreateAPIView):
    queryset = TaskManager.objects.select_related('position', 'employee').all()
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
        toplam_tapsiriq_sayi = queryset.aggregate(
            toplam = Count('id')
        ).get("toplam")
        tamamlandi = queryset.filter(status="Tamamlandı").aggregate(
            tamamlanan = Count('id')
        ).get("tamamlanan")
        icra_edilir = queryset.filter(status="İcra edilir").aggregate(
            icra_edilen = Count('id')
        ).get("icra_edilen")
        gecikir = queryset.filter(status="Gecikir").aggregate(
            geciken = Count('id')
        ).get("geciken")

        page = self.paginate_queryset(queryset)
        if page == None:
            page = queryset
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # serializer.data
            return self.get_paginated_response([{
                    'toplam_tapsiriq_sayi':toplam_tapsiriq_sayi,
                    'tamamlandi':tamamlandi,
                    'icra_edilir':icra_edilir,
                    'gecikir':gecikir,
                    'data':serializer.data
            }])
        serializer = self.get_serializer(queryset, many=True)
        return Response([{
                    'toplam_tapsiriq_sayi':toplam_tapsiriq_sayi,
                    'tamamlandi':tamamlandi,
                    'icra_edilir':icra_edilir,
                    'gecikir':gecikir,
                    'data':serializer.data
            }])
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            creator = request.user
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
                    position = Position.objects.get(pk=position_id)
                    users = User.objects.filter(position=position)
                    for user in users:
                        task_manager = TaskManager.objects.create(
                            creator = creator,
                            title = serializer.validated_data.get('title'),
                            body = serializer.validated_data.get('body'),
                            created_date = created_date,
                            end_date = end_date,
                            position = position,
                            employee = user,
                        )
                        task_manager.save()
            if user_list is not None:
                for user_id in user_list:
                    user = User.objects.get(pk=user_id)
                    task_manager = TaskManager.objects.create(
                        creator = creator,
                        title = serializer.validated_data.get('title'),
                        body = serializer.validated_data.get('body'),
                        created_date = created_date,
                        end_date = end_date,
                        employee = user,
                    )
                    task_manager.save()
            if user_list == None and position_list == None:
                return Response({'detail' : "İşçi və ya vəzifədən biri mütləq seçilməlidir"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Tapşırıq əlavə edildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail' : "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

class TaskManagerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskManager.objects.all()
    serializer_class = TaskManagerSerializer
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
        if serializer.is_valid():
            creator = request.user
            serializer.save(creator=creator)
            return Response({"detail": "Sorğu əlavə edildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)


class UserTaskRequestDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserTaskRequest.objects.all()
    serializer_class = UserTaskRequestSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            is_accept = serializer.validated_data.get("is_accept")
            new_date = instance.new_date
            task = instance.task
            if is_accept == True:
                task.end_date = new_date
                task.save()
                serializer.save()
            serializer.save()
            return Response({"detail": "Məlumatlar yeniləndi"})
        else:
            return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)


class AdvertisementListCreateAPIView(generics.ListCreateAPIView):
    queryset = Advertisement.objects.select_related('position').all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    permission_classes = [permissions.AdvertisementPermissions]
    
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        toplam_tapsiriq_quantityi = 0
        toplam_tapsiriq_quantityi = queryset.aggregate(
            toplam = Count('id')
        ).get("toplam")

        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([{
                    'toplam_tapsiriq_quantityi':toplam_tapsiriq_quantityi,
                    'data':serializer.data
            }])
        serializer = self.get_serializer(queryset, many=True)
        return Response([{
                    'toplam_tapsiriq_quantityi':toplam_tapsiriq_quantityi,
                    'data':serializer.data
            }])
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            creator = request.user
            position_str = serializer.validated_data.get("positions")
            if position_str is not None:
                position_list = position_str.split(',')
            else:
                position_list = None
            created_date = serializer.validated_data.get('created_date')
            if created_date == None:
                created_date = datetime.today()

            if position_list is not None:
                for position_id in position_list:
                    position = Position.objects.get(pk=position_id)
                    advertisement = Advertisement.objects.create(
                        creator = creator,
                        title = serializer.validated_data.get('title'),
                        body = serializer.validated_data.get('body'),
                        created_date = created_date,
                        position = position,
                    )
                    advertisement.save()
            else:
                serializer.save()
            return Response({"detail": "Elan əlavə edildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail' : "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)


class AdvertisementDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advertisement.objects.select_related('position').all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.AdvertisementPermissions]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail": "Məlumatlar yeniləndi"})
