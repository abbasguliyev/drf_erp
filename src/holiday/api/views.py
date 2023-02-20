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

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        extra = dict()
        all_working_day_count = 0
        all_const_salary = 0
        all_holiday = 0
        all_payed_days_off = 0
        all_unpayed_days_off = 0
        for q in page:
            emp = q.employee
            all_working_day_count += q.working_days_count
            all_const_salary += emp.salary
            total_holiday = employee_holiday_list().filter(employee = emp, holiday_date__month=q.date.month, holiday_date__year=q.date.year).count()
            total_payed_days_off = employee_day_off_list().filter(employee = emp, is_paid=True, day_off_date__month=q.date.month, day_off_date__year=q.date.year).count()
            total_unpayed_days_off = employee_day_off_list().filter(employee = emp, is_paid=False, day_off_date__month=q.date.month, day_off_date__year=q.date.year).count()
            all_holiday += total_holiday
            all_payed_days_off += total_payed_days_off
            all_unpayed_days_off += total_unpayed_days_off

            extra['all_working_day_count'] = int(all_working_day_count)
            extra['all_const_salary'] = int(all_const_salary)
            extra['all_holiday'] = int(all_holiday)
            extra['all_payed_days_off'] = int(all_payed_days_off)
            extra['all_unpayed_days_off'] = int(all_unpayed_days_off)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'extra': extra, 'data':serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
    permission_classes = [holiday_permissions.EmployeeHolidayHistoryPermissions]

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
            return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_201_CREATED)
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
    permission_classes = [holiday_permissions.EmployeeDayOffHistoryPermissions]
    
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
            return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
