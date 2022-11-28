from rest_framework import status, generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from holiday.api.serializers import (
    EmployeeWorkingDaySerializer,
    EmployeeHolidaySerializer,
    EmployeeHolidayHistorySerializer,
    HolidayOperationSerializer
)

from holiday.api import permissions as holiday_permissions

from holiday.api.selectors import (
    employee_working_day_list,
    employee_holiday_list,
    employee_holiday_history_list,
    holiday_operation_list
)

from holiday.api.services.holiday_services import (
    holiday_operation_create,
    employee_holiday_history_delete
)

from holiday.api.filters import (
    EmployeeWorkingDayFilter,
    EmployeeHolidayHistoryFilter,
    EmployeeHolidayFilter
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

class EmployeeHolidayHistoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = employee_holiday_history_list()
    serializer_class = EmployeeHolidayHistorySerializer
    permission_classes = [holiday_permissions.EmployeeHolidayHistoryPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        employee_holiday_history_delete(instance=instance)
        return Response({'detail': 'Silmə əməliyyatı yerinə yetirildi'}, status=status.HTTP_204_NO_CONTENT)


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
