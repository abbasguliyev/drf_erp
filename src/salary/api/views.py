from django.db.models import Sum, Q

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from salary.api.services.advancedpayment_service import advancepayment_create, advance_payment_update
from salary.api.services.bonus_service import bonus_create, bonus_delete, bonus_update
from salary.api.services.commission_services import (
    month_range_create,
    month_range_update,
    sale_range_create,
    sale_range_update,
    commission_installment_create,
    commission_sale_range_create,
    commission_create,
    commission_update
)
from salary.api.services.salary_pay_service import salary_pay_service
from salary.api.services.salarydeduction_service import salarydeduction_create, salary_deduction_update, salary_deduction_delete
from salary.api.services.salarypunishment_service import salarypunishment_create, salary_punishment_update, salary_punishment_delete

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
from holiday.api.selectors import employee_working_day_list
from contract.api.selectors import contract_list
from contract import CONTINUING, CANCELLED

User = get_user_model()

# ********************************** AdvancePayment endpoints **********************************


class AdvancePaymentListCreateAPIView(generics.ListCreateAPIView):
    queryset = advance_payment_list()
    serializer_class = AdvancePaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvancePaymentFilter
    permission_classes = [salary_permissions.AdvancePaymentPermissions]

    def get(self, request, *args, **kwargs):
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


class AdvancePaymentDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = advance_payment_list()
    serializer_class = AdvancePaymentSerializer
    permission_classes = [salary_permissions.AdvancePaymentPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            advance_payment_update(instance, **serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# ********************************** SalaryDeduction endpoints **********************************
class SalaryDeductionListCreateAPIView(generics.ListCreateAPIView):
    queryset = salary_deduction_list()
    serializer_class = SalaryDeductionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryDeductionFilter
    permission_classes = [salary_permissions.SalaryDeductionPermissions]

    def get(self, request, *args, **kwargs):
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


class SalaryDeductionDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = salary_deduction_list()
    serializer_class = SalaryDeductionSerializer
    permission_classes = [salary_permissions.SalaryDeductionPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            salary_deduction_update(instance, **serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SalaryDeductionDelete(APIView):
    permission_classes = [salary_permissions.SalaryDeductionPermissions]

    class InputSerializer(serializers.Serializer):
        instance_list = serializers.PrimaryKeyRelatedField(
            queryset=salary_deduction_list(), write_only=True, many=True
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        salary_deduction_delete(**serializer.validated_data, func_name='salary_deduction_delete')
        return Response({'detail': 'Silmə əməliyyatı yerinə yetirildi'}, status=status.HTTP_200_OK)

# ********************************** SalaryPunishment endpoints **********************************
class SalaryPunishmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = salary_punishment_list()
    serializer_class = SalaryPunishmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryPunishmentFilter
    permission_classes = [salary_permissions.SalaryPunishmentPermissions]

    def get(self, request, *args, **kwargs):
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
    queryset = salary_punishment_list()
    serializer_class = SalaryPunishmentSerializer
    permission_classes = [salary_permissions.SalaryPunishmentPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            salary_punishment_update(instance, **serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SalaryPunishmentDelete(APIView):
    permission_classes = [salary_permissions.SalaryPunishmentPermissions]

    class InputSerializer(serializers.Serializer):
        instance_list = serializers.PrimaryKeyRelatedField(
            queryset=salary_punishment_list(), write_only=True, many=True
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        salary_punishment_delete(**serializer.validated_data, func_name='salary_punishment_delete')
        return Response({'detail': 'Silmə əməliyyatı yerinə yetirildi'}, status=status.HTTP_200_OK)

# ********************************** Bonus endpoints **********************************
class BonusListCreateAPIView(generics.ListCreateAPIView):
    queryset = bonus_list()
    serializer_class = BonusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BonusFilter
    permission_classes = [salary_permissions.BonusPermissions]

    def get(self, request, *args, **kwargs):
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


class BonusDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = bonus_list()
    serializer_class = BonusSerializer
    permission_classes = [salary_permissions.BonusPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            bonus_update(instance, **serializer.validated_data)
            return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BonusDelete(APIView):
    permission_classes = [salary_permissions.BonusPermissions]
    
    class InputSerializer(serializers.Serializer):
        instance_list = serializers.PrimaryKeyRelatedField(
            queryset=bonus_list(), write_only=True, many=True
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bonus_delete(**serializer.validated_data, func_name='bonus_delete')
        return Response({'detail': 'Silmə əməliyyatı yerinə yetirildi'}, status=status.HTTP_200_OK)


# ********************************** Maas Ode endpoints **********************************
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
# ********************************** SalaryView endpoints **********************************
class SalaryViewListAPIView(generics.ListAPIView):
    queryset = salary_view_list()
    serializer_class = SalaryViewSerializer
    filterset_class = SalaryViewFilter
    permission_classes = [salary_permissions.SalaryViewPermissions]

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)

        extra = dict()
        all_bonus = 0
        all_advancepayment = 0
        all_salarydeduction = 0
        all_salarypunishment = 0
        all_final_salary = 0
        all_working_day = 0
        all_const_salary = 0
        all_sale_quantity = 0
        all_continuing_sale_quantity = 0
        all_falling_sale_quantity = 0
        all_commission = 0

        for q in page:
            month = q.date.month
            year = q.date.year
            total_working_day = employee_working_day_list().filter(employee=q.employee, date__month=month, date__year=year).last()
            e_history = employee_activity_history_list().filter(salary_view=q, activity_date__month = month, activity_date__year = year).last()
            continuing_sales = contract_list().filter(Q(group_leader=q.employee) | Q(manager1=q.employee) | Q(manager2=q.employee), contract_status=CONTINUING, contract_date__month=month, contract_date__year=year).count()
            falling_sales = contract_list().filter(Q(group_leader=q.employee) | Q(manager1=q.employee) | Q(manager2=q.employee), contract_status=CANCELLED, contract_date__month=month, contract_date__year=year).count()
            all_working_day += total_working_day.working_days_count
            all_bonus += e_history.bonus
            all_advancepayment += e_history.advance_payment
            all_salarydeduction += e_history.salary_deduction
            all_salarypunishment += e_history.salary_punishment
            all_final_salary += q.final_salary 
            all_const_salary += q.employee.salary
            all_sale_quantity += q.sale_quantity
            all_commission += q.commission_amount
            all_continuing_sale_quantity += continuing_sales
            all_falling_sale_quantity += falling_sales

        extra['all_bonus'] = int(all_bonus)
        extra['all_advancepayment'] = int(all_advancepayment)
        extra['all_salarydeduction'] = int(all_salarydeduction)
        extra['all_salarypunishment'] = int(all_salarypunishment)
        extra['all_final_salary'] = int(all_final_salary)
        extra['all_working_day'] = int(all_working_day)
        extra['all_const_salary'] = int(all_const_salary)
        extra['all_sale_quantity'] = int(all_sale_quantity)
        extra['all_commission'] = int(all_commission)
        extra['all_continuing_sale_quantity'] = int(all_continuing_sale_quantity)
        extra['all_falling_sale_quantity'] = int(all_falling_sale_quantity)

        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'extra': extra, 'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
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

# ********************************** Commission endpoints **********************************
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        month_range_update(instance, **serializer.validated_data)
        return Response({'detail': 'Ay aralığı məlumatları yeniləndi'}, status=status.HTTP_200_OK)


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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        sale_range_update(instance, **serializer.validated_data)
        return Response({'detail': 'Satış sayı aralığı məlumatları yeniləndi'}, status=status.HTTP_200_OK)


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