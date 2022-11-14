from api.v1.salary.services.advancedpayment_service import advancepayment_create
from api.v1.salary.services.bonus_service import bonus_create
from api.v1.salary.services.commission_services import (
    month_range_create,
    sale_range_create,
    commission_installment_create,
    commission_sale_range_create,
    commission_create,
    commission_update
)
from api.v1.salary.services.salary_pay_service import salary_pay_create
from api.v1.salary.services.salarydeduction_service import salarydeduction_create
from api.v1.salary.services.salarypunishment_service import salarypunishment_create

from salary.models import (
    AdvancePayment,
    SalaryDeduction,
    Bonus,
    SalaryPunishment,
    SalaryView,
    PaySalary,
    MonthRange, SaleRange, Commission, CommissionInstallment, CommissionSaleRange
)

from holiday.models import EmployeeWorkingDay

from api.v1.salary.serializers import (
    AdvancePaymentSerializer,
    BonusSerializer,
    SalaryDeductionSerializer,
    SalaryPunishmentSerializer,
    SalaryViewSerializer,
    SalaryOprSerializer,
    PaySalarySerializer,
    MonthRangeSerializer, SaleRangeSerializer, CommissionSerializer,
    CommissionInstallmentSerializer, CommissionSaleRangeSerializer,
)

from api.v1.account.serializers import UserSerializer

from rest_framework import status, generics

from rest_framework.response import Response

from api.v1.salary import permissions as salary_permissions

from django_filters.rest_framework import DjangoFilterBackend

from api.v1.salary.filters import (
    AdvancePaymentFilter,
    BonusFilter,
    SalaryDeductionFilter,
    SalaryPunishmentFilter,
    SalaryViewFilter,
    PaySalaryFilter,
)

import datetime
from django.db.models import Count, Q, Sum, Value
from itertools import groupby
from api.core import DynamicFieldsCategorySerializer
from rest_framework import serializers


from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from django.contrib.auth import get_user_model

User = get_user_model()

# ********************************** AdvancePayment get post put delete **********************************


class AdvancePaymentListCreateAPIView(generics.ListCreateAPIView):
    queryset = AdvancePayment.objects.select_related('employee').all()
    serializer_class = AdvancePaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvancePaymentFilter
    permission_classes = [salary_permissions.AdvancePaymentPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(employee__company=request.user.company,
                                                employee__office=request.user.office)
            queryset = self.queryset.filter(
                employee__company=request.user.company)
        else:
            queryset = self.queryset
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            user = request.user
            advancepayment_create(user, **serializer.validated_data)
            return Response({"detail": "Avans vermə əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AdvancePaymentDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = AdvancePayment.objects.all()
    serializer_class = AdvancePaymentSerializer
    permission_classes = [salary_permissions.AdvancePaymentPermissions]


# ********************************** SalaryDeduction get post put delete **********************************
class SalaryDeductionListCreateAPIView(generics.ListCreateAPIView):
    queryset = SalaryDeduction.objects.all()
    serializer_class = SalaryDeductionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryDeductionFilter
    permission_classes = [salary_permissions.SalaryDeductionPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = SalaryDeduction.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = SalaryDeduction.objects.filter(employee__company=request.user.company,
                                                          employee__office=request.user.office)
            queryset = SalaryDeduction.objects.filter(
                employee__company=request.user.company)
        else:
            queryset = SalaryDeduction.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            salarydeduction_create(**serializer.validated_data)
            return Response({"detail": "Kəsinti əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SalaryDeductionDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = SalaryDeduction.objects.all()
    serializer_class = SalaryDeductionSerializer
    permission_classes = [salary_permissions.SalaryDeductionPermissions]


# ********************************** SalaryPunishment get post put delete **********************************
class SalaryPunishmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = SalaryPunishment.objects.all()
    serializer_class = SalaryPunishmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryPunishmentFilter
    permission_classes = [salary_permissions.SalaryPunishmentPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(employee__company=request.user.company,
                                                employee__office=request.user.office)
            queryset = self.queryset.filter(
                employee__company=request.user.company)
        else:
            queryset = self.queryset
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            salarypunishment_create(**serializer.validated_data)
            return Response({"detail": "Cərimə əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SalaryPunishmentDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = SalaryPunishment.objects.all()
    serializer_class = SalaryPunishmentSerializer
    permission_classes = [salary_permissions.SalaryPunishmentPermissions]


# ********************************** Bonus get post put delete **********************************
class BonusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BonusFilter
    permission_classes = [salary_permissions.BonusPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Bonus.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = Bonus.objects.filter(employee__company=request.user.company,
                                                employee__office=request.user.office)
            queryset = Bonus.objects.filter(
                employee__company=request.user.company)
        else:
            queryset = Bonus.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            bonus_create(**serializer.validated_data)
            return Response({"detail": "Bonus əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BonusDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    permission_classes = [salary_permissions.BonusPermissions]


# ********************************** Maas Ode get post put delete **********************************
class PaySalaryListCreateAPIView(generics.ListCreateAPIView):
    queryset = PaySalary.objects.all()
    serializer_class = PaySalarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaySalaryFilter
    permission_classes = [salary_permissions.PaySalaryPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = PaySalary.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = PaySalary.objects.filter(employee__company=request.user.company,
                                                    employee__office=request.user.office)
            queryset = PaySalary.objects.filter(
                employee__company=request.user.company)
        else:
            queryset = PaySalary.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            user = request.user
            salary_pay_create(user, **serializer.validated_data)
            return Response({"detail": "Maaş ödəmə yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PaySalaryDetailAPIView(generics.RetrieveAPIView):
    queryset = PaySalary.objects.all()
    serializer_class = PaySalarySerializer
    permission_classes = [salary_permissions.PaySalaryPermissions]


# ********************************** SalaryView get post put delete **********************************
class SalaryViewListCreateAPIView(generics.ListAPIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        employee = UserSerializer(read_only=True, fields=['id', 'fullname', 'company', 'office', 'position', 'salary'])
        sale_quantity = serializers.IntegerField(read_only=True)
        commission_amount = serializers.FloatField(read_only=True)
        final_salary = serializers.FloatField(read_only=True)
        pay_date = serializers.DateField(read_only=True)
        is_done = serializers.BooleanField(read_only=True)
        salary_opr = SalaryOprSerializer(read_only=True)
        employee_working_day = serializers.IntegerField(read_only=True)
        date = serializers.DateField(read_only=True)
        

    queryset = SalaryView.objects.select_related('employee').all()
    serializer_class = SalaryViewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryViewFilter
    permission_classes = [salary_permissions.SalaryViewPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(employee__company=request.user.company,
                                                employee__office=request.user.office)
            queryset = self.queryset.filter(
                employee__company=request.user.company)
        else:
            queryset = self.queryset

        queryset = self.filter_queryset(queryset)

        start_date_qs = self.request.GET.get('start_date')
        end_date_qs = self.request.GET.get('end_date')

        if start_date_qs != "" and start_date_qs is not None:
            start_date = datetime.datetime.strptime(start_date_qs, "%d-%m-%Y")
            if end_date_qs != "" and end_date_qs is not None:
                end_date = datetime.datetime.strptime(end_date_qs, "%d-%m-%Y")
            else:
                end_date = datetime.date.today()
            
            new_queryset = queryset.filter(Q(date__month__gte=start_date.month), Q(date__year__gte=start_date.year), Q(
                date__month__lte=end_date.month), Q(date__year__lte=end_date.year)).order_by('employee__pk')
            new_qs_list = list()
            for qs in groupby(new_queryset.values('employee__pk')):
                new_qs_dict = dict()

                # print(f"{qs=}")
                employee_id = qs[0].get('employee__pk')
                employee = User.objects.get(pk=employee_id)
                date = qs[0].get('date')
                
                obj_opr = SalaryView.objects.filter(employee=employee, date__month__gte=start_date.month, date__year__gte=start_date.year, date__month__lte=end_date.month, date__year__lte=end_date.year).aggregate(
                    total_sale_quantity = Sum('sale_quantity'),
                    total_commission_amount = Sum('commission_amount'),
                    total_final_salary = Sum('final_salary')
                )

                salary_opr = User.objects.select_related(
                                            'holding', 'company', 'office', 'section', 'position', 'team', 'employee_status', 'department'
                                        ).filter(pk=employee.pk).values('pk').aggregate(
                                            total_advancepayment = Sum('advancepayment__amount', filter=(Q(advancepayment__date__month__gte=start_date.month, advancepayment__date__year__gte=start_date.year, advancepayment__date__month__lte=end_date.month, advancepayment__date__year__lte=end_date.year))),
                                            total_bonus = Sum('bonus__amount', filter=(Q(bonus__date__month__gte=start_date.month, bonus__date__year__gte=start_date.year, bonus__date__month__lte=end_date.month, bonus__date__year__lte=end_date.year))), 
                                            total_salarydeduction = Sum('salarydeduction__amount', filter=(Q(salarydeduction__date__month__gte=start_date.month, salarydeduction__date__year__gte=start_date.year, salarydeduction__date__month__lte=end_date.month, salarydeduction__date__year__lte=end_date.year))),
                                            total_salarypunishment = Sum('salarypunishment__amount', filter=(Q(salarypunishment__date__month__gte=start_date.month, salarypunishment__date__year__gte=start_date.year, salarypunishment__date__month__lte=end_date.month, salarypunishment__date__year__lte=end_date.year))),
                                        )
                working_day = User.objects.select_related(
                                            'holding', 'company', 'office', 'section', 'position', 'team', 'employee_status', 'department'
                                        ).filter(pk=employee.pk).values('pk').aggregate(
                                            total_working_day=Sum('working_days__working_days_count', filter=(Q(working_days__date__month__gte=start_date.month, working_days__date__year__gte=start_date.year, working_days__date__month__lte=end_date.month, working_days__date__year__lte=end_date.year))),
                                        )
                if obj_opr.get('total_sale_quantity') is None:
                    obj_opr['total_sale_quantity'] = 0
                else:
                    obj_opr['total_sale_quantity'] = int(obj_opr['total_sale_quantity'])
                
                if obj_opr.get('total_commission_amount') is None:
                    obj_opr['total_commission_amount'] = 0
                else:
                    obj_opr['total_commission_amount'] = int(obj_opr['total_commission_amount'])

                if obj_opr.get('total_final_salary') is None:
                    obj_opr['total_final_salary'] = 0
                else:
                    obj_opr['total_final_salary'] = int(obj_opr['total_final_salary'])
                     
                if working_day.get('total_working_day') is None:
                    working_day['total_working_day'] = 0
                else:
                    working_day['total_working_day'] = int(working_day['total_working_day'])
                                        
                if salary_opr.get("total_advancepayment") is None:
                    salary_opr['total_advancepayment'] = 0
                else:
                    salary_opr['total_advancepayment'] = int(salary_opr['total_advancepayment'])
                
                if salary_opr.get("total_bonus") is None:
                    salary_opr['total_bonus'] = 0
                else:
                    salary_opr['total_bonus'] = int(salary_opr['total_bonus'])
                
                if salary_opr.get("total_salarydeduction") is None:
                    salary_opr['total_salarydeduction'] = 0
                else:
                    salary_opr['total_salarydeduction'] = int(salary_opr['total_salarydeduction'])
                
                if salary_opr.get("total_salarypunishment") is None:
                    salary_opr['total_salarypunishment'] = 0
                else:
                    salary_opr['total_salarypunishment'] = int(salary_opr['total_salarypunishment'])            

                print(f"user_id=>{qs[0].get('employee__pk')} -> bonus=>{salary_opr.get('total_bonus')}, avans=>{salary_opr.get('total_advancepayment')}, kəsinti=>{salary_opr.get('total_salarydeduction')}, cərimə=>{salary_opr.get('total_salarypunishment')}, iş günü=>{salary_opr.get('total_working_day')}")
                new_qs_dict['id'] = qs[0].get('employee__pk')
                new_qs_dict['employee'] = employee
                new_qs_dict['salary_opr'] = salary_opr
                new_qs_dict['date'] = date
                new_qs_dict['employee_working_day'] = working_day['total_working_day']
                new_qs_dict['sale_quantity'] = obj_opr['total_sale_quantity']
                new_qs_dict['commission_amount'] = obj_opr['total_commission_amount']
                new_qs_dict['final_salary'] = obj_opr['total_final_salary']
                new_qs_dict['is_done'] = False
                new_qs_dict['pay_date'] = None
                new_qs_dict['date'] = None
                
                new_qs_list.append(new_qs_dict)
            page = self.paginate_queryset(new_qs_list)
            if page is not None:
                new_serializer = self.OutputSerializer
                serializer = new_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


class SalaryViewDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = SalaryView.objects.all()
    serializer_class = SalaryViewSerializer
    permission_classes = [salary_permissions.SalaryViewPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)


# ********************************** Commission get post put delete **********************************
class MonthRangeListCreateAPIView(generics.ListCreateAPIView):
    queryset = MonthRange.objects.all()
    serializer_class = MonthRangeSerializer
    permission_classes = [salary_permissions.MonthRangePermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            month_range_create(**serializer.validated_data)
            return Response({"detail": "Ay aralığı əlavə edildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MonthRangeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MonthRange.objects.all()
    serializer_class = MonthRangeSerializer
    permission_classes = [salary_permissions.MonthRangePermissions]


class SaleRangeListCreateAPIView(generics.ListCreateAPIView):
    queryset = SaleRange.objects.all()
    serializer_class = SaleRangeSerializer
    permission_classes = [salary_permissions.SaleRangePermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            sale_range_create(**serializer.validated_data)
            return Response({"detail": "Satış sayı aralığı əlavə edildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SaleRangeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SaleRange.objects.all()
    serializer_class = SaleRangeSerializer
    permission_classes = [salary_permissions.SaleRangePermissions]


class CommissionInstallmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = CommissionInstallment.objects.all()
    serializer_class = CommissionInstallmentSerializer
    # permission_classes = [salary_permissions.CommissionInstallmentPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            commission_installment_create(**serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommissionInstallmentDetailAPIView(generics.ListCreateAPIView):
    queryset = CommissionInstallment.objects.all()
    serializer_class = CommissionInstallmentSerializer
    # permission_classes = [salary_permissions.CommissionInstallmentPermissions]


class CommissionSaleRangeListCreateAPIView(generics.ListCreateAPIView):
    queryset = CommissionSaleRange.objects.all()
    serializer_class = CommissionSaleRangeSerializer
    # permission_classes = [salary_permissions.CommissionSaleRangePermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            commission_sale_range_create(**serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommissionSaleRangeDetailAPIView(generics.ListCreateAPIView):
    queryset = CommissionSaleRange.objects.all()
    serializer_class = CommissionSaleRangeSerializer
    # permission_classes = [salary_permissions.CommissionSaleRangePermissions]


class CommissionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = [salary_permissions.CommissionPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            commission_create(**serializer.validated_data)
            return Response({"detail": "Komissiya əlavə edildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommissionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = [salary_permissions.CommissionPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            commission_update(instance.id, **serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
