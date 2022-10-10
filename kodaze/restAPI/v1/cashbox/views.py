from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend

from restAPI.v1.cashbox.utils import (
    calculate_holding_total_balance, 
    cashflow_create, 
    calculate_office_balance, 
    calculate_company_balance, 
    calculate_holding_balance
)
from rest_framework.response import Response

from restAPI.v1.cashbox.serializers import (
    CashFlowSerializer,
    HoldingCashboxSerializer,
    CompanyCashboxSerializer,
    OfficeCashboxSerializer,
)

from cashbox.models import (
    HoldingCashbox,
    CompanyCashbox,
    OfficeCashbox,
    CashFlow
)

from restAPI.v1.cashbox.filters import (
    HoldingCashboxFilter,
    OfficeCashboxFilter,
    CashFlowFilter,
    CompanyCashboxFilter,
)

from restAPI.v1.cashbox import permissions as company_permissions
from django.contrib.auth.models import Group
# ********************************** kassa put delete post get **********************************

class HoldingCashboxListCreateAPIView(generics.ListCreateAPIView):
    queryset = HoldingCashbox.objects.all()
    serializer_class = HoldingCashboxSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingCashboxFilter
    permission_classes = [company_permissions.HoldingCashboxPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            holding = serializer.validated_data.get("holding")
            balance = serializer.validated_data.get("balance")

            initial_balance = calculate_holding_total_balance()
            holding_initial_balance = calculate_holding_balance()

            serializer.save()

            subsequent_balance = calculate_holding_total_balance()
            holding_subsequent_balance = calculate_holding_balance()
            cashflow_create(
                holding=holding,
                description=f"{holding.name} holdinq kassasına {float(balance)} AZN əlavə edildi",
                initial_balance=initial_balance,
                subsequent_balance=subsequent_balance,
                holding_initial_balance=holding_initial_balance,
                holding_subsequent_balance=holding_subsequent_balance,
                executor=user,
                quantity=float(balance)
            )
            return Response({"detail":"Holding kassa əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)



class HoldingCashboxDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = HoldingCashbox.objects.all()
    serializer_class = HoldingCashboxSerializer
    permission_classes = [company_permissions.HoldingCashboxPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        user = request.user
        if serializer.is_valid():
            holding = instance.holding

            initial_balance = calculate_holding_total_balance()
            holding_initial_balance = calculate_holding_balance()

            balance = serializer.validated_data.get("balance")

            serializer.save()

            subsequent_balance = calculate_holding_total_balance()
            holding_subsequent_balance = calculate_holding_balance()
            cashflow_create(
                holding=holding,
                description=f"{holding.name} holdinq kassasına {float(balance)} AZN əlavə edildi",
                initial_balance=initial_balance,
                subsequent_balance=subsequent_balance,
                holding_initial_balance=holding_initial_balance,
                holding_subsequent_balance=holding_subsequent_balance,
                executor=user,
                quantity=float(balance)
            )
            return Response({"detail":"Holding kassa məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)



# **********************************

class CompanyCashboxListCreateAPIView(generics.ListCreateAPIView):
    queryset = CompanyCashbox.objects.select_related('company').all()
    serializer_class = CompanyCashboxSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyCashboxFilter
    permission_classes = [company_permissions.CompanyCashboxPermissions]

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            company = serializer.validated_data.get("company")
            balance = serializer.validated_data.get("balance")

            initial_balance = calculate_holding_total_balance()
            company_initial_balance = calculate_company_balance(company=company)

            serializer.save()

            subsequent_balance = calculate_holding_total_balance()
            company_subsequent_balance = calculate_company_balance(company=company)
            cashflow_create(
                company=company,
                description=f"{company.name} şirkət kassasına {float(balance)} AZN əlavə edildi",
                initial_balance=initial_balance,
                subsequent_balance=subsequent_balance,
                company_initial_balance=company_initial_balance,
                company_subsequent_balance=company_subsequent_balance,
                executor=user,
                quantity=float(balance)
            )
            return Response({"detail":"Şirkət kassa əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)



class CompanyCashboxDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = CompanyCashbox.objects.select_related('company').all()
    serializer_class = CompanyCashboxSerializer
    permission_classes = [company_permissions.CompanyCashboxPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        user = request.user
        if serializer.is_valid():
            company = instance.company

            balance = serializer.validated_data.get("balance")
            initial_balance = calculate_holding_total_balance()
            company_initial_balance = calculate_company_balance(company=company)

            serializer.save()
            
            subsequent_balance = calculate_holding_total_balance()
            company_subsequent_balance = calculate_company_balance(company=company)
            cashflow_create(
                company=company,
                description=f"{company.name} şirkət kassasına {float(balance)} AZN əlavə edildi",
                initial_balance=initial_balance,
                subsequent_balance=subsequent_balance,
                company_initial_balance=company_initial_balance,
                company_subsequent_balance=company_subsequent_balance,
                executor=user,
                quantity=float(balance)
            )
            return Response({"detail":"Şirkət kassa məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)



# **********************************

class OfficeCashboxListCreateAPIView(generics.ListCreateAPIView):
    queryset = OfficeCashbox.objects.select_related('office').all()
    serializer_class = OfficeCashboxSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeCashboxFilter
    permission_classes = [company_permissions.OfficeCashboxPermissions]

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            office = serializer.validated_data.get("office")
            balance = serializer.validated_data.get("balance")

            initial_balance = calculate_holding_total_balance()
            office_initial_balance = calculate_office_balance(office=office)

            serializer.save()

            subsequent_balance = calculate_holding_total_balance()
            office_subsequent_balance = calculate_office_balance(office=office)
            cashflow_create(
                office=office,
                company=office.company,
                description=f"{office.name} office kassasına {float(balance)} AZN əlavə edildi",
                initial_balance=initial_balance,
                subsequent_balance=subsequent_balance,
                office_initial_balance=office_initial_balance,
                office_subsequent_balance=office_subsequent_balance,
                executor=user,
                quantity=float(balance)
            )
            return Response({"detail":"Office kassa əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)



class OfficeCashboxDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = OfficeCashbox.objects.select_related('office').all()
    serializer_class = OfficeCashboxSerializer
    permission_classes = [company_permissions.OfficeCashboxPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        user = request.user
        if serializer.is_valid():
            office = instance.office
            balance = serializer.validated_data.get("balance")
            
            initial_balance = calculate_holding_total_balance()
            office_initial_balance = calculate_office_balance(office=office)

            serializer.save()
            
            subsequent_balance = calculate_holding_total_balance()
            office_subsequent_balance = calculate_office_balance(office=office)
            cashflow_create(
                office=office,
                company=office.company,
                description=f"{office.name} office kassasına {float(balance)} AZN əlavə edildi",
                initial_balance=initial_balance,
                subsequent_balance=subsequent_balance,
                office_initial_balance=office_initial_balance,
                office_subsequent_balance=office_subsequent_balance,
                executor=user,
                quantity=float(balance)
            )
            return Response({"detail":"Office kassa məlumatları yeniləndi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

# ********************************** Pul Axini get **********************************

class CashFlowListAPIView(generics.ListAPIView):
    queryset = CashFlow.objects.select_related('holding', 'company', 'office', 'executor').all()
    serializer_class = CashFlowSerializer
    permission_classes = [company_permissions.CashFlowPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CashFlowFilter

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # umumi_quantity = queryset.count()
        umumi_quantity = 0

        for q in queryset:
            umumi_quantity += q.quantity

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'umumi_quantity': umumi_quantity, 'data':serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return Response([
                {'umumi_quantity': umumi_quantity, 'data':serializer.data}
            ])

class CashFlowDetailAPIView(generics.RetrieveAPIView):
    queryset = CashFlow.objects.select_related('holding', 'company', 'office', 'executor').all()
    serializer_class = CashFlowSerializer
    permission_classes = [company_permissions.CashFlowPermissions]