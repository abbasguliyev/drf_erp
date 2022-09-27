import django_filters

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
    PositionWorkingDay,
    HoldingExceptionWorker,
    PositionExceptionWorker,
    SectionExceptionWorker
)


class EmployeeArrivalAndDepartureTimesFilter(django_filters.FilterSet):
    class Meta:
        model = EmployeeArrivalAndDepartureTimes
        fields = {
            'employee__fullname': ['exact', 'icontains'],
            'arrival_time': ['exact', 'gte', 'lte'],
            'departure_time': ['exact', 'gte', 'lte'],
        }


class EmployeeWorkingDayFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = EmployeeWorkingDay
        fields = {
            'employee__id': ['exact'],
            'employee__fullname': ['exact', 'icontains'],
            'working_days_count': ['exact', 'gte', 'lte'],
            'non_working_days_count': ['exact', 'gte', 'lte'],
            'holidays': ['exact', 'icontains'],
            'paid_leave_days': ['exact', 'icontains'],
            'unpaid_leave_days': ['exact', 'icontains'],
            # 'date': ['exact', 'gte', 'lte'],
        }


class HoldingWorkingDayFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = HoldingWorkingDay
        fields = {
            'holding__name': ['exact', 'icontains'],
            'working_days_count': ['exact', 'gte', 'lte'],
            'non_working_days_count': ['exact', 'gte', 'lte'],
            'holidays': ['exact', 'icontains'],
            # 'date': ['exact', 'gte', 'lte'],
        }


class CompanyWorkingDayFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = CompanyWorkingDay
        fields = {
            'company__name': ['exact', 'icontains'],
            'working_days_count': ['exact', 'gte', 'lte'],
            'non_working_days_count': ['exact', 'gte', 'lte'],
            'holidays': ['exact', 'icontains'],
            # 'date': ['exact', 'gte', 'lte'],
        }


class OfficeWorkingDayFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = OfficeWorkingDay
        fields = {
            'office__id': ['exact'],
            'office__name': ['exact', 'icontains'],
            'working_days_count': ['exact', 'gte', 'lte'],
            'non_working_days_count': ['exact', 'gte', 'lte'],
            'holidays': ['exact', 'icontains'],
            # 'date': ['exact', 'gte', 'lte'],
        }


class SectionWorkingDayFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = SectionWorkingDay
        fields = {
            'section__id': ['exact'],
            'section__name': ['exact', 'icontains'],
            'working_days_count': ['exact', 'gte', 'lte'],
            'non_working_days_count': ['exact', 'gte', 'lte'],
            'holidays': ['exact', 'icontains'],
            # 'date': ['exact', 'gte', 'lte'],
        }


class TeamWorkingDayFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = TeamWorkingDay
        fields = {
            'team__name': ['exact', 'icontains'],
            'working_days_count': ['exact', 'gte', 'lte'],
            'non_working_days_count': ['exact', 'gte', 'lte'],
            'holidays': ['exact', 'icontains'],
            # 'date': ['exact', 'gte', 'lte'],
        }


class PositionWorkingDayFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(
        field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(
        field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = PositionWorkingDay
        fields = {
            'position__name': ['exact', 'icontains'],
            'working_days_count': ['exact', 'gte', 'lte'],
            'non_working_days_count': ['exact', 'gte', 'lte'],
            'holidays': ['exact', 'icontains'],
            # 'date': ['exact', 'gte', 'lte'],
        }


class TeamExceptionWorkerFilter(django_filters.FilterSet):
    working_day__date = django_filters.DateFilter(
        field_name='working_day__date', input_formats=["%d-%m-%Y"])
    working_day__date__gte = django_filters.DateFilter(
        field_name='working_day__date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    working_day__date__lte = django_filters.DateFilter(
        field_name='working_day__date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = TeamExceptionWorker
        fields = {
            'working_day__team__name': ['exact', 'icontains'],
            'working_day__working_days_count': ['exact', 'gte', 'lte'],
            'working_day__non_working_days_count': ['exact', 'gte', 'lte'],
            'working_day__holidays': ['exact', 'icontains'],
            # 'working_day__date': ['exact', 'gte', 'lte'],
        }


class OfficeExceptionWorkerFilter(django_filters.FilterSet):
    working_day__date = django_filters.DateFilter(
        field_name='working_day__date', input_formats=["%d-%m-%Y"])
    working_day__date__gte = django_filters.DateFilter(
        field_name='working_day__date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    working_day__date__lte = django_filters.DateFilter(
        field_name='working_day__date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = OfficeExceptionWorker
        fields = {
            'working_day__office__id': ['exact'],
            'working_day__office__name': ['exact', 'icontains'],
            'working_day__working_days_count': ['exact', 'gte', 'lte'],
            'working_day__non_working_days_count': ['exact', 'gte', 'lte'],
            'working_day__holidays': ['exact', 'icontains'],
            # 'working_day__date': ['exact', 'gte', 'lte'],
        }


class CompanyExceptionWorkerFilter(django_filters.FilterSet):
    working_day__date = django_filters.DateFilter(
        field_name='working_day__date', input_formats=["%d-%m-%Y"])
    working_day__date__gte = django_filters.DateFilter(
        field_name='working_day__date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    working_day__date__lte = django_filters.DateFilter(
        field_name='working_day__date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = CompanyExceptionWorker
        fields = {
            'working_day__company__name': ['exact', 'icontains'],
            'working_day__working_days_count': ['exact', 'gte', 'lte'],
            'working_day__non_working_days_count': ['exact', 'gte', 'lte'],
            'working_day__holidays': ['exact', 'icontains'],
            # 'working_day__date': ['exact', 'gte', 'lte'],
        }


class HoldingExceptionWorkerFilter(django_filters.FilterSet):
    working_day__date = django_filters.DateFilter(
        field_name='working_day__date', input_formats=["%d-%m-%Y"])
    working_day__date__gte = django_filters.DateFilter(
        field_name='working_day__date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    working_day__date__lte = django_filters.DateFilter(
        field_name='working_day__date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = HoldingExceptionWorker
        fields = {
            'working_day__holding__name': ['exact', 'icontains'],
            'working_day__working_days_count': ['exact', 'gte', 'lte'],
            'working_day__non_working_days_count': ['exact', 'gte', 'lte'],
            'working_day__holidays': ['exact', 'icontains'],
            # 'working_day__date': ['exact', 'gte', 'lte'],
        }


class PositionExceptionWorkerFilter(django_filters.FilterSet):
    working_day__date = django_filters.DateFilter(
        field_name='working_day__date', input_formats=["%d-%m-%Y"])
    working_day__date__gte = django_filters.DateFilter(
        field_name='working_day__date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    working_day__date__lte = django_filters.DateFilter(
        field_name='working_day__date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = PositionExceptionWorker
        fields = {
            'working_day__position__name': ['exact', 'icontains'],
            'working_day__working_days_count': ['exact', 'gte', 'lte'],
            'working_day__non_working_days_count': ['exact', 'gte', 'lte'],
            'working_day__holidays': ['exact', 'icontains'],
            # 'working_day__date': ['exact', 'gte', 'lte'],
        }


class SectionExceptionWorkerFilter(django_filters.FilterSet):
    working_day__date = django_filters.DateFilter(
        field_name='working_day__date', input_formats=["%d-%m-%Y"])
    working_day__date__gte = django_filters.DateFilter(
        field_name='working_day__date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    working_day__date__lte = django_filters.DateFilter(
        field_name='working_day__date', lookup_expr='lte', input_formats=["%d-%m-%Y"])

    class Meta:
        model = SectionExceptionWorker
        fields = {
            'working_day__section__id': ['exact'],
            'working_day__section__name': ['exact', 'icontains'],
            'working_day__section__name': ['exact', 'icontains'],
            'working_day__working_days_count': ['exact', 'gte', 'lte'],
            'working_day__non_working_days_count': ['exact', 'gte', 'lte'],
            'working_day__holidays': ['exact', 'icontains'],
            # 'working_day__date': ['exact', 'gte', 'lte'],
        }
