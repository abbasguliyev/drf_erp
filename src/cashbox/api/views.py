from rest_framework import status, generics
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from contract.api.selectors import installment_list
from contract.api.filters import InstallmentFilter
from contract.api import permissions as contract_permissions
from contract.api.serializers import InstallmentSerializer
from contract import FINISHED

from services.api.selectors import service_list
from services.api.serializers import ServicePaymentSerializer

from services.api.selectors import service_list, service_payment_list

from services.api.filters import ServicePaymentFilter
from services.api import permissions as service_permissions

from cashbox.api.serializers import (
    CashFlowSerializer,
    HoldingCashboxSerializer,
    CompanyCashboxSerializer,
    OfficeCashboxSerializer,
    HoldingCashboxOperationSerializer,
    CompanyCashboxOperationSerializer,
    CostTypeSerializer
)

from cashbox.api.filters import (
    HoldingCashboxFilter,
    OfficeCashboxFilter,
    CashFlowFilter,
    CompanyCashboxFilter,
    HoldingCashboxOperationFilter,
    CompanyCashboxOperationFilter,
    CostTypeFilter
)

from cashbox.api import permissions as cashbox_permissions
from cashbox.api.services import (
    cashbox_operation_services,
    cashbox_services,
    cost_type_services
)
from cashbox.api.selectors import (
    holding_cashbox_list,
    company_cashbox_list,
    office_cashbox_list,
    cash_flow_list,
    holding_cashbox_opr_list,
    company_cashbox_opr_list,
    cost_type_list
)

# ********************************** kassa endpoints **********************************

class HoldingCashboxListCreateAPIView(generics.ListAPIView):
    queryset = holding_cashbox_list()
    serializer_class = HoldingCashboxSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingCashboxFilter
    permission_classes = [cashbox_permissions.HoldingCashboxPermissions]


class HoldingCashboxDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = holding_cashbox_list()
    serializer_class = HoldingCashboxSerializer
    permission_classes = [cashbox_permissions.HoldingCashboxPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            cashbox_services.update_holding_cashbox_service(user, instance, **serializer.validated_data)
            return Response({"detail":"Holding kassa məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)


# **********************************

class CompanyCashboxListCreateAPIView(generics.ListAPIView):
    queryset = company_cashbox_list()
    serializer_class = CompanyCashboxSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyCashboxFilter
    permission_classes = [cashbox_permissions.CompanyCashboxPermissions]

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CompanyCashboxDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = company_cashbox_list()
    serializer_class = CompanyCashboxSerializer
    permission_classes = [cashbox_permissions.CompanyCashboxPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            cashbox_services.update_company_cashbox_service(user, instance, **serializer.validated_data)
            return Response({"detail":"Şirkət kassa məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)



# **********************************

class OfficeCashboxListCreateAPIView(generics.ListAPIView):
    queryset = office_cashbox_list()
    serializer_class = OfficeCashboxSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeCashboxFilter
    permission_classes = [cashbox_permissions.OfficeCashboxPermissions]

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class OfficeCashboxDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = office_cashbox_list()
    serializer_class = OfficeCashboxSerializer
    permission_classes = [cashbox_permissions.OfficeCashboxPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            cashbox_services.update_office_cashbox_service(user, instance, **serializer.validated_data)
            return Response({"detail":"Office kassa məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

# ********************************** Pul Axini endpoints **********************************

class CashFlowListAPIView(generics.ListAPIView):
    queryset = cash_flow_list()
    serializer_class = CashFlowSerializer
    permission_classes = [cashbox_permissions.CashFlowPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CashFlowFilter

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        extra = dict()
        total_quantity = 0
        total_balance = 0
        for q in page:
            total_quantity += q.quantity
            total_balance += q.balance

            extra['total_quantity'] = int(total_quantity)
            extra['total_balance'] = int(total_balance)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'extra': extra, 'data':serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return Response([
                {'extra': extra, 'data':serializer.data}
            ])

class CashFlowDetailAPIView(generics.RetrieveAPIView):
    queryset = cash_flow_list()
    serializer_class = CashFlowSerializer
    permission_classes = [cashbox_permissions.CashFlowPermissions]


class HoldingCashboxOperationListCreateAPIView(generics.ListCreateAPIView):
    queryset = holding_cashbox_opr_list()
    serializer_class = HoldingCashboxOperationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingCashboxOperationFilter
    permission_classes = [cashbox_permissions.HoldingCashboxOperationPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            cashbox_operation_services.holding_cashbox_operation_create(executor=user, **serializer.validated_data)
            return Response({"detail":"Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CompanyCashboxOperationListCreateAPIView(generics.ListCreateAPIView):
    queryset = company_cashbox_opr_list()
    serializer_class = CompanyCashboxOperationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyCashboxOperationFilter
    permission_classes = [cashbox_permissions.CompanyCashboxOperationPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            cashbox_operation_services.company_cashbox_operation_create(executor=user, **serializer.validated_data)
            return Response({"detail":"Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CostTypeListApiView(generics.ListAPIView):
    queryset = cost_type_list()
    serializer_class = CostTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CostTypeFilter
    permission_classes = [cashbox_permissions.CostTypePermissions]

class CostTypeCreateApiView(generics.CreateAPIView):
    queryset = cost_type_list()
    serializer_class = CostTypeSerializer
    permission_classes = [cashbox_permissions.CostTypePermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cost_type_services.create_cost_type(**serializer.validated_data)
        return Response({'detail': 'Xərc növü əlavə edildi'}, status=status.HTTP_201_CREATED)

class CostTypeDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = cost_type_list()
    serializer_class = CostTypeSerializer
    permission_classes = [cashbox_permissions.CostTypePermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        cost_type_services.update_cost_type(instance=instance, **serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_200_OK)



class InstallmentPaymentTrackingListAPIView(generics.ListAPIView):
    queryset = installment_list().order_by('date')
    serializer_class = InstallmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = InstallmentFilter
    permission_classes = [contract_permissions.InstallmentPermissions]

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)

        extra = dict()
        total_price = 0
        total_paid_amount = 0
        total_remaining_debt = 0
        total_service_debt = 0
        total_debt = 0

        for q in page:
            if q.is_paid == True:
                total_paid_amount += q.paid_price

        unique_contracts = set(d.contract for d in page)

        for unique_contract in unique_contracts:
            services = service_list().filter(contract=unique_contract)
            for service in services:
                total_service_debt += service.remaining_payment

            total_remaining_debt = total_remaining_debt + unique_contract.remaining_debt
            total_price = total_price + unique_contract.total_amount
            total_paid_amount += unique_contract.paid_initial_payment
            if unique_contract.initial_payment_debt_status == FINISHED:
                total_paid_amount += unique_contract.paid_initial_payment_debt
            
        total_debt = total_remaining_debt + total_service_debt

        extra['total_price'] = int(total_price)
        # extra['total_price'] = total_price + total_service_debt
        extra['total_paid_amount'] = int(total_paid_amount)
        extra['total_remaining_debt'] = int(total_remaining_debt)
        extra['total_service_debt'] = int(total_service_debt)
        extra['total_debt'] = int(total_debt)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'extra': extra, 'data': serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response([
            {'extra': extra, 'data': serializer.data}
        ])


class ServicePaymentTrackingListAPIView(generics.ListAPIView):
    queryset = service_payment_list().order_by("payment_date")
    serializer_class = ServicePaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServicePaymentFilter
    permission_classes = [service_permissions.ServicePermissions]

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        extra = dict()

        all_price = 0
        all_total_paid_amount = 0
        total_service_debt = 0

        for q in page:
            all_price += q.service_amount
            all_total_paid_amount += q.service_paid_amount
        
        unique_services = set(d.service for d in page)

        for unique_service in unique_services:
            services = service_list().filter(pk=unique_service.pk)
            for service in services:
                total_service_debt += service.remaining_payment
            
        extra['all_price'] = int(all_price)
        extra['all_total_paid_amount'] = int(all_total_paid_amount)
        extra['all_remaining_payment'] = int(total_service_debt)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'extra': extra, 'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)