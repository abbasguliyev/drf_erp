from rest_framework import status, generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from holiday.api.serializers import (
    EmployeeWorkingDaySerializer,
    EmployeeHolidaySerializer,
    EmployeeHolidayHistorySerializer,
    HolidayOperationSerializer,
    EmployeeDayOffHistorySerializer,
    EmployeeDayOffSerializer,
    EmployeeDayOffOperationSerializer
)

from holiday.api import permissions as holiday_permissions

from holiday.api.selectors import (
    employee_working_day_list,
    employee_holiday_list,
    employee_holiday_history_list,
    holiday_operation_list,
    employee_day_off_list,
    employee_day_off_history_list,
    employee_day_off_operation_list
)

from holiday.api.services.holiday_services import (
    holiday_operation_create,
    holiday_history_delete_service,
    employee_holiday_history_update
)

from holiday.api.services.day_off_services import (
    employee_day_off_operation_create,
    days_off_history_delete_service,
    employee_day_off_history_update
)

from holiday.api.filters import (
    EmployeeWorkingDayFilter,
    EmployeeHolidayHistoryFilter,
    EmployeeHolidayFilter,
    EmployeeDayOffFilter,
    EmployeeDayOffHistoryFilter
)

class EmployeeWorkingDayListAPIView(generics.ListAPIView):
    queryset = employee_working_day_list()
    serializer_class = EmployeeWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeWorkingDayFilter
    permission_classes = [holiday_permissions.EmployeeWorkingDayPermissions]

class EmployeeHolidayListAPIView(generics.ListAPIView):
    queryset = employee_holiday_list()
    serializer_class = EmployeeHolidaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeHolidayFilter
    permission_classes = [holiday_permissions.EmployeeHolidayPermissions]

class EmployeeHolidayHistoryListAPIView(generics.ListAPIView):
    queryset = employee_holiday_history_list()
    serializer_class = EmployeeHolidayHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeHolidayHistoryFilter
    permission_classes = [holiday_permissions.EmployeeHolidayHistoryPermissions]

class EmployeeHolidayHistoryDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = employee_holiday_history_list()
    serializer_class = EmployeeHolidayHistorySerializer
    permission_classes = [holiday_permissions.EmployeeHolidayHistoryPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            employee_holiday_history_update(instance, **serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeHolidayHistoryDelete(APIView):
    class InputSerializer(serializers.Serializer):
        instance_list = serializers.PrimaryKeyRelatedField(
            queryset=employee_holiday_history_list(), write_only=True, many=True
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        holiday_history_delete_service(**serializer.validated_data)
        return Response({'detail': 'Silmə əməliyyatı yerinə yetirildi'}, status=status.HTTP_200_OK)



class HolidayOperationListCreateAPIView(generics.ListCreateAPIView):
    queryset = holiday_operation_list()
    serializer_class = HolidayOperationSerializer
    permission_classes = [holiday_permissions.HolidayOperationPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            holiday_operation_create(**serializer.validated_data)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDayOffListAPIView(generics.ListAPIView):
    queryset = employee_day_off_list()
    serializer_class = EmployeeDayOffSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeDayOffFilter
    permission_classes = [holiday_permissions.EmployeeDayOffPermissions]

class EmployeeDayOffHistoryListAPIView(generics.ListAPIView):
    queryset = employee_day_off_history_list()
    serializer_class = EmployeeDayOffHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeDayOffHistoryFilter
    permission_classes = [holiday_permissions.EmployeeDayOffHistoryPermissions]

class EmployeeDayOffHistoryDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = employee_day_off_history_list()
    serializer_class = EmployeeDayOffHistorySerializer
    permission_classes = [holiday_permissions.EmployeeDayOffHistoryPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            employee_day_off_history_update(instance, **serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDayOffHistoryDelete(APIView):
    class InputSerializer(serializers.Serializer):
        instance_list = serializers.PrimaryKeyRelatedField(
            queryset=employee_day_off_history_list(), write_only=True, many=True
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        days_off_history_delete_service(**serializer.validated_data)
        return Response({'detail': 'Silmə əməliyyatı yerinə yetirildi'}, status=status.HTTP_200_OK)


class EmployeeDayOffOperationListCreateAPIView(generics.ListCreateAPIView):
    queryset = employee_day_off_operation_list()
    serializer_class = EmployeeDayOffOperationSerializer
    permission_classes = [holiday_permissions.EmployeeDayOffOperationPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            employee_day_off_operation_create(**serializer.validated_data)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
