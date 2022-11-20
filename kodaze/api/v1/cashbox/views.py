from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

from api.v1.cashbox.serializers import (
    CashFlowSerializer,
    HoldingCashboxSerializer,
    CompanyCashboxSerializer,
    OfficeCashboxSerializer,
    HoldingCashboxOperationSerializer,
    CompanyCashboxOperationSerializer
)

from cashbox.models import (
    HoldingCashbox,
    CompanyCashbox,
    OfficeCashbox,
    CashFlow,
    HoldingCashboxOperation,
    CompanyCashboxOperation
)

from api.v1.cashbox.filters import (
    HoldingCashboxFilter,
    OfficeCashboxFilter,
    CashFlowFilter,
    CompanyCashboxFilter,
    HoldingCashboxOperationFilter,
    CompanyCashboxOperationFilter
)

from api.v1.cashbox import permissions as cashbox_permissions
from api.v1.cashbox.services import (
    cashbox_operation_services,
    cashbox_services
)

# ********************************** kassa put delete post get **********************************

class HoldingCashboxListCreateAPIView(generics.ListAPIView):
    queryset = HoldingCashbox.objects.all()
    serializer_class = HoldingCashboxSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingCashboxFilter
    permission_classes = [cashbox_permissions.HoldingCashboxPermissions]


class HoldingCashboxDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = HoldingCashbox.objects.all()
    serializer_class = HoldingCashboxSerializer
    permission_classes = [cashbox_permissions.HoldingCashboxPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            cashbox_services.update_cashbox_service(instance=instance, data=serializer.validated_data)
            return Response({"detail":"Holding kassa məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)


# **********************************

class CompanyCashboxListCreateAPIView(generics.ListAPIView):
    queryset = CompanyCashbox.objects.select_related('company').all()
    serializer_class = CompanyCashboxSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyCashboxFilter
    permission_classes = [cashbox_permissions.CompanyCashboxPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            queryset = self.queryset.filter(company=request.user.company)
        else:
            queryset = self.queryset
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CompanyCashboxDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = CompanyCashbox.objects.select_related('company').all()
    serializer_class = CompanyCashboxSerializer
    permission_classes = [cashbox_permissions.CompanyCashboxPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            cashbox_services.update_cashbox_service(instance=instance, data=serializer.validated_data)
            return Response({"detail":"Şirkət kassa məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)



# **********************************

class OfficeCashboxListCreateAPIView(generics.ListAPIView):
    queryset = OfficeCashbox.objects.select_related('office').all()
    serializer_class = OfficeCashboxSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeCashboxFilter
    permission_classes = [cashbox_permissions.OfficeCashboxPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(office__company=request.user.company, office=request.user.office)
            queryset = self.queryset.filter(office__company=request.user.company)
        else:
            queryset = self.queryset
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class OfficeCashboxDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = OfficeCashbox.objects.select_related('office').all()
    serializer_class = OfficeCashboxSerializer
    permission_classes = [cashbox_permissions.OfficeCashboxPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            cashbox_services.update_cashbox_service(instance=instance, data=serializer.validated_data)
            return Response({"detail":"Office kassa məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

# ********************************** Pul Axini get **********************************

class CashFlowListAPIView(generics.ListAPIView):
    queryset = CashFlow.objects.select_related('holding', 'company', 'office', 'executor').all()
    serializer_class = CashFlowSerializer
    permission_classes = [cashbox_permissions.CashFlowPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CashFlowFilter

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        total_quantity = 0

        for q in queryset:
            total_quantity += q.quantity

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'total_quantity': total_quantity, 'data':serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return Response([
                {'total_quantity': total_quantity, 'data':serializer.data}
            ])

class CashFlowDetailAPIView(generics.RetrieveAPIView):
    queryset = CashFlow.objects.select_related('holding', 'company', 'office', 'executor').all()
    serializer_class = CashFlowSerializer
    permission_classes = [cashbox_permissions.CashFlowPermissions]


class HoldingCashboxOperationListCreateAPIView(generics.ListCreateAPIView):
    queryset = HoldingCashboxOperation.objects.all()
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
    queryset = CompanyCashboxOperation.objects.all()
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

