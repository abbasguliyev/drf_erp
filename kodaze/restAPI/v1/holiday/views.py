from restAPI.v1.holiday.serializers import (
    HoldingWorkingDaySerializer,
    EmployeeArrivalAndDepartureTimesSerializer, 
    EmployeeWorkingDaySerializer, 
    TeamWorkingDaySerializer,
    TeamExceptionWorkerSerializer, 
    OfficeWorkingDaySerializer,
    OfficeExceptionWorkerSerializer, 
    CompanyWorkingDaySerializer,
    CompanyExceptionWorkerSerializer, 
    SectionWorkingDaySerializer,
    SectionExceptionWorkerSerializer, 
    PositionWorkingDaySerializer,
    HoldingExceptionWorkerSerializer,
    PositionExceptionWorkerSerializer
)
from holiday.models import (
    HoldingWorkingDay,
    EmployeeArrivalAndDepartureTimes,
    EmployeeWorkingDay,
    TeamWorkingDay,
    TeamExceptionWorker,
    OfficeWorkingDay,
    OfficeExceptionWorker,
    CompanyWorkingDay,
    CompanyExceptionWorker,
    SectionWorkingDay,
    SectionExceptionWorker,
    PositionWorkingDay,
    HoldingExceptionWorker,
    PositionExceptionWorker
)

from rest_framework.response import Response

from restAPI.v1.holiday import utils as working_day_utils

from rest_framework import generics

from restAPI.v1.holiday import permissions as working_day_permissions

from django_filters.rest_framework import DjangoFilterBackend

from restAPI.v1.holiday.filters import (
    HoldingWorkingDayFilter,
    HoldingExceptionWorkerFilter,
    EmployeeArrivalAndDepartureTimesFilter,
    EmployeeWorkingDayFilter,
    TeamWorkingDayFilter,
    TeamExceptionWorkerFilter,
    OfficeWorkingDayFilter,
    OfficeExceptionWorkerFilter,
    CompanyWorkingDayFilter,
    CompanyExceptionWorkerFilter,
    SectionWorkingDayFilter,
    SectionExceptionWorkerFilter,
    PositionWorkingDayFilter,
    PositionExceptionWorkerFilter,
) 
from rest_framework import status

# ********************************** Holding Gunler get post put delete **********************************
class HoldingWorkingDayListCreateAPIView(generics.ListAPIView):
    queryset = HoldingWorkingDay.objects.all()
    serializer_class = HoldingWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingWorkingDayFilter
    permission_classes = [working_day_permissions.HoldingWorkingDayPermissions]

class HoldingWorkingDayDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HoldingWorkingDay.objects.all()
    serializer_class = HoldingWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingWorkingDayFilter
    permission_classes = [working_day_permissions.HoldingWorkingDayPermissions]

    def update(self, request, *args, **kwargs):
        return working_day_utils.holding_working_day_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

class HoldingExceptionWorkerListCreateAPIView(generics.ListCreateAPIView):
    queryset = HoldingExceptionWorker.objects.all()
    serializer_class = HoldingExceptionWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingExceptionWorkerFilter
    permission_classes = [working_day_permissions.HoldingExceptionWorkerPermissions]

    def create(self, request, *args, **kwargs):
        return working_day_utils.holding_exception_worker_working_day_create(self, request, *args, **kwargs)

class HoldingExceptionWorkerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HoldingExceptionWorker.objects.all()
    serializer_class = HoldingExceptionWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingExceptionWorkerFilter
    permission_classes = [working_day_permissions.HoldingExceptionWorkerPermissions]

    def update(self, request, *args, **kwargs):
        return working_day_utils.holding_exception_worker_working_day_update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return working_day_utils.holding_exception_worker_working_day_delete(self, request, *args, **kwargs)

# ********************************** Company Gunler get post put delete **********************************
class CompanyWorkingDayListCreateAPIView(generics.ListAPIView):
    queryset = CompanyWorkingDay.objects.all()
    serializer_class = CompanyWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyWorkingDayFilter
    permission_classes = [working_day_permissions.CompanyWorkingDayPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = CompanyWorkingDay.objects.all()
        elif request.user.company is not None:
            queryset = CompanyWorkingDay.objects.filter(company=request.user.company)
        else:
            queryset = CompanyWorkingDay.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CompanyWorkingDayDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyWorkingDay.objects.all()
    serializer_class = CompanyWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyWorkingDayFilter
    permission_classes = [working_day_permissions.CompanyWorkingDayPermissions]

    def update(self, request, *args, **kwargs):
        return working_day_utils.company_working_day_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

class CompanyExceptionWorkerListCreateAPIView(generics.ListCreateAPIView):
    queryset = CompanyExceptionWorker.objects.all()
    serializer_class = CompanyExceptionWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyExceptionWorkerFilter
    permission_classes = [working_day_permissions.CompanyExceptionWorkerPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = CompanyExceptionWorker.objects.all()
        elif request.user.company is not None:
            queryset = CompanyExceptionWorker.objects.filter(working_day__company=request.user.company)
        else:
            queryset = CompanyExceptionWorker.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return working_day_utils.company_exception_worker_working_day_create(self, request, *args, **kwargs)

class CompanyExceptionWorkerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyExceptionWorker.objects.all()
    serializer_class = CompanyExceptionWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyExceptionWorkerFilter
    permission_classes = [working_day_permissions.CompanyExceptionWorkerPermissions]

    def update(self, request, *args, **kwargs):
        return working_day_utils.company_exception_worker_working_day_update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return working_day_utils.company_exception_worker_working_day_delete(self, request, *args, **kwargs)

# ********************************** Office Gunler get post put delete **********************************
class OfficeWorkingDayListCreateAPIView(generics.ListAPIView):
    queryset = OfficeWorkingDay.objects.all()
    serializer_class = OfficeWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeWorkingDayFilter
    permission_classes = [working_day_permissions.OfficeWorkingDayPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = OfficeWorkingDay.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = OfficeWorkingDay.objects.filter(office__company=request.user.company, office=request.user.office)
            queryset = OfficeWorkingDay.objects.filter(office__company=request.user.company)
        else:
            queryset = OfficeWorkingDay.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OfficeWorkingDayDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OfficeWorkingDay.objects.all()
    serializer_class = OfficeWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeWorkingDayFilter
    permission_classes = [working_day_permissions.OfficeWorkingDayPermissions]

    def update(self, request, *args, **kwargs):
        return working_day_utils.office_working_day_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

class OfficeExceptionWorkerListCreateAPIView(generics.ListCreateAPIView):
    queryset = OfficeExceptionWorker.objects.all()
    serializer_class = OfficeExceptionWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeExceptionWorkerFilter
    permission_classes = [working_day_permissions.OfficeExceptionWorkerPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = OfficeExceptionWorker.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = OfficeExceptionWorker.objects.filter(working_day__office__company=request.user.company, working_day__office=request.user.office)
            queryset = OfficeExceptionWorker.objects.filter(working_day__office__company=request.user.company)
        else:
            queryset = OfficeExceptionWorker.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return working_day_utils.office_exception_worker_working_day_create(self, request, *args, **kwargs)

class OfficeExceptionWorkerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OfficeExceptionWorker.objects.all()
    serializer_class = OfficeExceptionWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeExceptionWorkerFilter
    permission_classes = [working_day_permissions.OfficeExceptionWorkerPermissions]

    def update(self, request, *args, **kwargs):
        return working_day_utils.office_exception_worker_working_day_update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return working_day_utils.office_exception_worker_working_day_delete(self, request, *args, **kwargs)

# ********************************** Section Gunler get post put delete **********************************
class SectionWorkingDayListCreateAPIView(generics.ListAPIView):
    queryset = SectionWorkingDay.objects.all()
    serializer_class = SectionWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SectionWorkingDayFilter
    permission_classes = [working_day_permissions.SectionWorkingDayPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = SectionWorkingDay.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = SectionWorkingDay.objects.filter(section__office__company=request.user.company, section__office=request.user.office)
            queryset = SectionWorkingDay.objects.filter(section__office__company=request.user.company)
        else:
            queryset = SectionWorkingDay.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SectionWorkingDayDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SectionWorkingDay.objects.all()
    serializer_class = SectionWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SectionWorkingDayFilter
    permission_classes = [working_day_permissions.SectionWorkingDayPermissions]

    def update(self, request, *args, **kwargs):
        return working_day_utils.section_working_day_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

class SectionExceptionWorkerListCreateAPIView(generics.ListCreateAPIView):
    queryset = SectionExceptionWorker.objects.all()
    serializer_class = SectionExceptionWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SectionExceptionWorkerFilter
    permission_classes = [working_day_permissions.SectionExceptionWorkerPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = SectionExceptionWorker.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = SectionExceptionWorker.objects.filter(working_day__section__office__company=request.user.company, working_day__section__office=request.user.office)
            queryset = SectionExceptionWorker.objects.filter(working_day__section__office__company=request.user.company)
        else:
            queryset = SectionExceptionWorker.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return working_day_utils.section_exception_worker_working_day_create(self, request, *args, **kwargs)

class SectionExceptionWorkerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SectionExceptionWorker.objects.all()
    serializer_class = SectionExceptionWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SectionExceptionWorkerFilter
    permission_classes = [working_day_permissions.SectionExceptionWorkerPermissions]

    def update(self, request, *args, **kwargs):
        return working_day_utils.section_exception_worker_working_day_update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return working_day_utils.section_exception_worker_working_day_delete(self, request, *args, **kwargs)

# ********************************** Team Gunler get post put delete **********************************
class TeamWorkingDayListCreateAPIView(generics.ListAPIView):
    queryset = TeamWorkingDay.objects.all()
    serializer_class = TeamWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeamWorkingDayFilter
    permission_classes = [working_day_permissions.TeamWorkingDayPermissions]


class TeamWorkingDayDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamWorkingDay.objects.all()
    serializer_class = TeamWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeamWorkingDayFilter
    permission_classes = [working_day_permissions.TeamWorkingDayPermissions]

    def update(self, request, *args, **kwargs):
        return working_day_utils.team_working_day_update(self, request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

class TeamExceptionWorkerListCreateAPIView(generics.ListCreateAPIView):
    queryset = TeamExceptionWorker.objects.all()
    serializer_class = TeamExceptionWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeamExceptionWorkerFilter
    permission_classes = [working_day_permissions.TeamExceptionWorkerPermissions]

    def create(self, request, *args, **kwargs):
        return working_day_utils.team_exception_worker_working_day_create(self, request, *args, **kwargs)

class TeamExceptionWorkerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamExceptionWorker.objects.all()
    serializer_class = TeamExceptionWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeamExceptionWorkerFilter
    permission_classes = [working_day_permissions.TeamExceptionWorkerPermissions]

    def update(self, request, *args, **kwargs):
        return working_day_utils.team_exception_worker_working_day_update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return working_day_utils.team_exception_worker_working_day_delete(self, request, *args, **kwargs)

# ********************************** Position Gunler get post put delete **********************************
class PositionWorkingDayListCreateAPIView(generics.ListAPIView):
    queryset = PositionWorkingDay.objects.all()
    serializer_class = PositionWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PositionWorkingDayFilter
    permission_classes = [working_day_permissions.PositionWorkingDayPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = PositionWorkingDay.objects.all()
        elif request.user.company is not None:
            queryset = PositionWorkingDay.objects.filter(position__company=request.user.company)
        else:
            queryset = PositionWorkingDay.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PositionWorkingDayDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PositionWorkingDay.objects.all()
    serializer_class = PositionWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PositionWorkingDayFilter
    permission_classes = [working_day_permissions.PositionWorkingDayPermissions]

    def update(self, request, *args, **kwargs):
        return working_day_utils.position_working_day_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

class PositionExceptionWorkerListCreateAPIView(generics.ListCreateAPIView):
    queryset = PositionExceptionWorker.objects.all()
    serializer_class = PositionExceptionWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PositionExceptionWorkerFilter
    permission_classes = [working_day_permissions.PositionExceptionWorkerPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = PositionExceptionWorker.objects.all()
        elif request.user.company is not None:
            queryset = PositionExceptionWorker.objects.filter(working_day__position__company=request.user.company)
        else:
            queryset = PositionExceptionWorker.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return working_day_utils.position_exception_worker_working_day_create(self, request, *args, **kwargs)

class PositionExceptionWorkerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PositionExceptionWorker.objects.all()
    serializer_class = PositionExceptionWorkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PositionExceptionWorkerFilter
    permission_classes = [working_day_permissions.PositionExceptionWorkerPermissions]

    def update(self, request, *args, **kwargs):
        return working_day_utils.position_exception_worker_working_day_update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return working_day_utils.position_exception_worker_working_day_delete(self, request, *args, **kwargs)
    
# ********************************** Isci Gunler get post put delete **********************************
class EmployeeWorkingDayListCreateAPIView(generics.ListAPIView):
    queryset = EmployeeWorkingDay.objects.all()
    serializer_class = EmployeeWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeWorkingDayFilter
    permission_classes = [working_day_permissions.EmployeeWorkingDayPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = EmployeeWorkingDay.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = EmployeeWorkingDay.objects.filter(employee__company=request.user.company, employee__office=request.user.office)
            queryset = EmployeeWorkingDay.objects.filter(employee__company=request.user.company)
        else:
            queryset = EmployeeWorkingDay.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeWorkingDayDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeWorkingDay.objects.all()
    serializer_class = EmployeeWorkingDaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeWorkingDayFilter
    permission_classes = [working_day_permissions.EmployeeWorkingDayPermissions]

    def update(self, request, *args, **kwargs):
        return working_day_utils.user_working_day_update(self, request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return working_day_utils.user_working_day_patch(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return working_day_utils.user_working_day_delete(self, request, *args, **kwargs)

# ********************************** Isci Gelib getme vaxtlari get post put delete **********************************
class EmployeeArrivalAndDepartureTimesListCreateAPIView(generics.ListCreateAPIView):
    queryset = EmployeeArrivalAndDepartureTimes.objects.all()
    serializer_class = EmployeeArrivalAndDepartureTimesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeArrivalAndDepartureTimesFilter
    permission_classes = [working_day_permissions.EmployeeArrivalAndDepartureTimesPermissions]

class EmployeeArrivalAndDepartureTimesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeArrivalAndDepartureTimes.objects.all()
    serializer_class = EmployeeArrivalAndDepartureTimesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeArrivalAndDepartureTimesFilter
    permission_classes = [working_day_permissions.EmployeeArrivalAndDepartureTimesPermissions]
