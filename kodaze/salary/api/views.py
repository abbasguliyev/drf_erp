from salary.api.services.advancedpayment_service import advancepayment_create, advance_payment_delete
from salary.api.services.bonus_service import bonus_create, bonus_delete
from salary.api.services.commission_services import (
    month_range_create,
    sale_range_create,
    commission_installment_create,
    commission_sale_range_create,
    commission_create,
    commission_update
)
from salary.api.services.salary_pay_service import salary_pay_service
from salary.api.services.salarydeduction_service import salarydeduction_create, salary_deduction_delete
from salary.api.services.salarypunishment_service import salarypunishment_create, salary_punishment_delete
from salary.api.utils import salary_operation_delete

from salary.models import (
    MonthRange, SaleRange, Commission, CommissionInstallment, CommissionSaleRange,
    SalaryViewExport
)

from salary.api.serializers import (
    AdvancePaymentSerializer,
    BonusSerializer,
    SalaryDeductionSerializer,
    SalaryPunishmentSerializer,
    SalaryViewSerializer,
    PaySalarySerializer,
    MonthRangeSerializer, SaleRangeSerializer, CommissionSerializer,
    CommissionInstallmentSerializer, CommissionSaleRangeSerializer,
    EmployeeActivityHistorySerializer
)
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from salary.api import permissions as salary_permissions


from salary.api.filters import (
    AdvancePaymentFilter,
    BonusFilter,
    SalaryDeductionFilter,
    SalaryPunishmentFilter,
    SalaryViewFilter,
    EmployeeActivityHistoryFilter
)

from salary.api.selectors import (
    advance_payment_list,
    salary_deduction_list,
    salary_punishment_list,
    bonus_list,
    pay_salary_list,
    salary_view_list,
    employee_activity_history_list
)

from salary.api.export_excell import export_salary_view

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from django.contrib.auth import get_user_model

User = get_user_model()

# ********************************** AdvancePayment get post put delete **********************************


class AdvancePaymentListCreateAPIView(generics.ListCreateAPIView):
    queryset = advance_payment_list()
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
            advancepayment_create(executor=user, **serializer.validated_data)
            return Response({"detail": "Avans vermə əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AdvancePaymentDetailAPIView(generics.RetrieveAPIView):
    queryset = advance_payment_list()
    serializer_class = AdvancePaymentSerializer
    permission_classes = [salary_permissions.AdvancePaymentPermissions]


# ********************************** SalaryDeduction get post put delete **********************************
class SalaryDeductionListCreateAPIView(generics.ListCreateAPIView):
    queryset = salary_deduction_list()
    serializer_class = SalaryDeductionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryDeductionFilter
    permission_classes = [salary_permissions.SalaryDeductionPermissions]

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
        if serializer.is_valid():
            salarydeduction_create(**serializer.validated_data)
            return Response({"detail": "Kəsinti əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SalaryDeductionDetailAPIView(generics.RetrieveAPIView):
    queryset = salary_deduction_list()
    serializer_class = SalaryDeductionSerializer
    permission_classes = [salary_permissions.SalaryDeductionPermissions]


class SalaryDeductionDelete(APIView):
    class InputSerializer(serializers.Serializer):
        instance_list_id = serializers.PrimaryKeyRelatedField(
            queryset=salary_deduction_list(), write_only=True, many=True
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        salary_deduction_delete(**serializer.validated_data, func_name='salary_deduction_delete')
        return Response({'detail': 'Silmə əməliyyatı yerinə yetirildi'}, status=status.HTTP_204_NO_CONTENT)

# ********************************** SalaryPunishment get post put delete **********************************
class SalaryPunishmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = salary_punishment_list()
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


class SalaryPunishmentDetailAPIView(generics.RetrieveAPIView):
    queryset = salary_punishment_list()
    serializer_class = SalaryPunishmentSerializer
    permission_classes = [salary_permissions.SalaryPunishmentPermissions]

class SalaryPunishmentDelete(APIView):
    class InputSerializer(serializers.Serializer):
        instance_list = serializers.PrimaryKeyRelatedField(
            queryset=salary_punishment_list(), write_only=True, many=True
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        salary_punishment_delete(**serializer.validated_data, func_name='salary_punishment_delete')
        return Response({'detail': 'Silmə əməliyyatı yerinə yetirildi'}, status=status.HTTP_204_NO_CONTENT)

# ********************************** Bonus get post put delete **********************************
class BonusListCreateAPIView(generics.ListCreateAPIView):
    queryset = bonus_list()
    serializer_class = BonusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BonusFilter
    permission_classes = [salary_permissions.BonusPermissions]

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
            bonus_create(**serializer.validated_data)
            return Response({"detail": "Bonus əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BonusDetailAPIView(generics.RetrieveAPIView):
    queryset = bonus_list()
    serializer_class = BonusSerializer
    permission_classes = [salary_permissions.BonusPermissions]


class BonusDelete(APIView):
    class InputSerializer(serializers.Serializer):
        instance_list = serializers.PrimaryKeyRelatedField(
            queryset=bonus_list(), write_only=True, many=True
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bonus_delete(**serializer.validated_data, func_name='bonus_delete')
        return Response({'detail': 'Silmə əməliyyatı yerinə yetirildi'}, status=status.HTTP_204_NO_CONTENT)


# ********************************** Maas Ode get post put delete **********************************
class PaySalaryCreateAPIView(generics.CreateAPIView):
    queryset = pay_salary_list()
    serializer_class = PaySalarySerializer
    permission_classes = [salary_permissions.PaySalaryPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            user = request.user
            salary_pay_service(executor=user, **serializer.validated_data)
            return Response({"detail": "Maaş ödəmə yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
# ********************************** SalaryView get post put delete **********************************
class SalaryViewListAPIView(generics.ListAPIView):
    queryset = salary_view_list()
    serializer_class = SalaryViewSerializer
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

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


class SalaryViewDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = salary_view_list()
    serializer_class = SalaryViewSerializer
    permission_classes = [salary_permissions.SalaryViewPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)


class ExportData(generics.CreateAPIView):
    class InputSerializer(serializers.Serializer):
        data = serializers.JSONField()

    queryset = SalaryViewExport.objects.all()
    serializer_class = InputSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            result = export_salary_view(**serializer.validated_data)
            data = result.path
            return Response({'file': f"{data}"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
    queryset = CommissionInstallment.objects.select_related('month_range').all()
    serializer_class = CommissionInstallmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            commission_installment_create(**serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommissionInstallmentDetailAPIView(generics.ListCreateAPIView):
    queryset = CommissionInstallment.objects.select_related('month_range').all()
    serializer_class = CommissionInstallmentSerializer


class CommissionSaleRangeListCreateAPIView(generics.ListCreateAPIView):
    queryset = CommissionSaleRange.objects.select_related('sale_range').all()
    serializer_class = CommissionSaleRangeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            commission_sale_range_create(**serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommissionSaleRangeDetailAPIView(generics.ListCreateAPIView):
    queryset = CommissionSaleRange.objects.select_related('sale_range').all()
    serializer_class = CommissionSaleRangeSerializer


class CommissionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Commission.objects.prefetch_related('installment', 'for_sale_range').all()
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
    queryset = Commission.objects.prefetch_related('installment', 'for_sale_range').all()
    serializer_class = CommissionSerializer
    permission_classes = [salary_permissions.CommissionPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            commission_update(instance, **serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class EmployeeActivityListAPIView(generics.ListAPIView):
    queryset = employee_activity_history_list()
    serializer_class = EmployeeActivityHistorySerializer
    filterset_class = EmployeeActivityHistoryFilter