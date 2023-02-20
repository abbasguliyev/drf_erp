from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from contract.api.services import (
    installment_create_service, 
    installment_update_service, 
    contract_create_service, 
    contract_update_service
)

from contract.api.serializers import (
    DemoSalesSerializer,
    ContractSerializer,
    ContractCreateSerializer,
    ContractGiftSerializer,
    InstallmentSerializer,
    ContractCreditorSerializer
)

from contract.models import (
    ContractCreditor,
    DemoSales
)

from contract.api.filters import (
    DemoSalesFilter,
    ContractGiftFilter,
    InstallmentFilter,
    ContractFilter,
    ContractCreditorFilter
)

from contract.api.services import (
    contract_gift_service,
    contract_creditor_service,
    contract_change_service,
)
from contract import FINISHED
from contract.tasks import pay_installment_task
from contract.api import permissions as contract_permissions
from contract.api.selectors import contract_list, contract_gift_list, installment_list, contract_creditor_list, demo_sales_list
from product.api.selectors import product_list
from account.api.selectors import region_list
from services.api.selectors import service_list

from django.db import transaction

# ********************************** contract endpoints **********************************


class ContractListAPIView(generics.ListAPIView):
    queryset = contract_list()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilter
    permission_classes = [contract_permissions.ContractPermissions]

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ContractCreateAPIView(generics.CreateAPIView):
    queryset = contract_list()
    serializer_class = ContractCreateSerializer
    permission_classes = [contract_permissions.ContractPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        contract = contract_create_service.create_contract(
            user=user, **serializer.validated_data)
        return Response({'detail': 'Müqavilə imzalandı', 'id': contract.id}, status=status.HTTP_201_CREATED)


class ContractDetailAPIView(generics.RetrieveAPIView):
    queryset = contract_list()
    serializer_class = ContractSerializer
    permission_classes = [contract_permissions.ContractPermissions]

class ContractUpdateAPIView(APIView):
    permission_classes = [contract_permissions.ContractPermissions]
    class InputSerializer(serializers.Serializer):
        region = serializers.PrimaryKeyRelatedField(
            queryset=region_list(), write_only=True, required=False
        )
        address = serializers.CharField(required=False)
        note = serializers.CharField(required=False)
        conditional_contract_note = serializers.CharField(required=False)
    
    def post(self, request, pk):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contract_update_service.update_contract(instance=id, **serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_200_OK)


class PayInitialPaymentDebtAPIView(APIView):
    permission_classes = [contract_permissions.ContractPermissions]
    
    class InputSerializer(serializers.Serializer):
        contract = serializers.PrimaryKeyRelatedField(
            queryset=contract_list(), write_only=True
        )
        initial_payment_amount = serializers.DecimalField(max_digits=20, decimal_places=0)
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        contract_update_service.pay_initial_payment_debt(user=user, **serializer.validated_data, func_name="pay_initial_payment_debt")
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_200_OK)


class RemoveProductAPIView(APIView):
    permission_classes = [contract_permissions.ContractPermissions]

    class InputSerializer(serializers.Serializer):
        contract = serializers.PrimaryKeyRelatedField(
            queryset=contract_list(), write_only=True
        )
        compensation_income = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        compensation_expense = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        note = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        contract_update_service.remove_contract(user=user, **serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_200_OK)


# ********************************** installment put endpoints **********************************


class InstallmentListAPIView(generics.ListAPIView):
    queryset = installment_list()
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

class InstallmentDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = installment_list()
    serializer_class = InstallmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contract']
    filterset_class = InstallmentFilter
    permission_classes = [contract_permissions.InstallmentPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = request.user
        installment_update_service.installment_update(
            user=user, instance=instance, **serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_200_OK)

class PayInstallmentAPIView(APIView):
    permission_classes = [contract_permissions.InstallmentPermissions]

    class InputSerializer(serializers.Serializer):
        installments = serializers.PrimaryKeyRelatedField(
            queryset=installment_list(), write_only=True, many=True
        )
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        installment_instances = serializer.validated_data.get("installments")
        installments = [inst.id for inst in installment_instances]
        transaction.on_commit(lambda: pay_installment_task.delay(user.id, installments))
        # installment_update_service.pay_total_installment(user=user, **serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_200_OK)


# ********************************** gift endpoints **********************************


class ContractGiftListAPIView(generics.ListAPIView):
    queryset = contract_gift_list()
    serializer_class = ContractGiftSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractGiftFilter
    permission_classes = [contract_permissions.ContractGiftPermissions]

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ContractGiftCreateAPIView(APIView):
    permission_classes = [contract_permissions.ContractGiftPermissions]

    class InputSerializer(serializers.Serializer):
        products = serializers.PrimaryKeyRelatedField(
            queryset=product_list(), write_only=True, many=True
        )
        quantities = serializers.CharField()
        contract = serializers.PrimaryKeyRelatedField(
            queryset=contract_list(), write_only=True
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        contract_gift_service.contract_gift_create(user=user, **serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_201_CREATED)


class ContractGiftDetailAPIView(generics.RetrieveAPIView):
    queryset = contract_gift_list()
    serializer_class = ContractGiftSerializer
    permission_classes = [contract_permissions.ContractGiftPermissions]
    
# ********************************** ContractChange endpoints **********************************


class ContractChangeListCreateAPIView(APIView):
    permission_classes = [contract_permissions.ContractPermissions]
    class InputSerializer(serializers.Serializer):
        old_contract = serializers.PrimaryKeyRelatedField(
            queryset=contract_list(), write_only=True
        )
        product = serializers.PrimaryKeyRelatedField(
            queryset=product_list(), write_only=True
        )
        initial_payments = serializers.DecimalField(max_digits=20, decimal_places=0)
        loan_term = serializers.IntegerField()
        discount = serializers.DecimalField(max_digits=20, decimal_places=0)
        note = serializers.CharField(required=False, allow_null=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        contract_change_service.change_contract_product_service(user=user, **serializer.validated_data)
        return Response({'detail': "Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)

class FindContractPaidAmout(APIView):
    permission_classes = [contract_permissions.ContractPermissions]
    class InputSerializer(serializers.Serializer):
        contract = serializers.PrimaryKeyRelatedField(
            queryset=contract_list(), write_only=True
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        paid_amount = contract_change_service.find_contract_paid_amount(**serializer.validated_data)
        return Response({'data': paid_amount}, status=status.HTTP_200_OK)


# ********************************** demo sale endpoints **********************************


class DemoSalesListAPIView(generics.ListAPIView):
    queryset = demo_sales_list()
    serializer_class = DemoSalesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DemoSalesFilter
    permission_classes = [contract_permissions.DemoSalesPermissions]


class DemoSalesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = demo_sales_list()
    serializer_class = DemoSalesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DemoSalesFilter
    permission_classes = [contract_permissions.DemoSalesPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            count_q = serializer.validated_data.get("count")
            count = instance.count + count_q
            serializer.save(count=count)
            return Response({"detail": "Demo əlavə olundu"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)


class CreateTestInstallmentAPIView(APIView):
    permission_classes = [contract_permissions.InstallmentPermissions]

    class InputSerializer(serializers.Serializer):
        loan_term = serializers.IntegerField()
        product_quantity = serializers.IntegerField()
        installment_start_date = serializers.DateField()
        initial_payment = serializers.DecimalField(required=False, allow_null=True, max_digits=20, decimal_places=0)
        initial_payment_debt = serializers.DecimalField(required=False, allow_null=True, max_digits=20, decimal_places=0)
        product_id = serializers.IntegerField()
        discount = serializers.DecimalField(required=False, allow_null=True, max_digits=20, decimal_places=0)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        total_installment = installment_create_service.create_test_installment(**serializer.validated_data)
        return Response({'data': total_installment}, status=status.HTTP_200_OK)


class ContractCreditorListCreateAPIView(generics.ListCreateAPIView):
    queryset = contract_creditor_list()
    serializer_class = ContractCreditorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractCreditorFilter
    permission_classes = [contract_permissions.ContractCreditorPermissions]

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
        serializer.is_valid(raise_exception=True)
        contract_creditor_service.contract_creditor_create(
            **serializer.validated_data)
        return Response({'detail': 'Kreditor əlavə olundu'}, status=status.HTTP_201_CREATED)


class ContractCreditorDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = contract_creditor_list()
    serializer_class = ContractCreditorSerializer
    permission_classes = [contract_permissions.ContractCreditorPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Kreditor məlumatları yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)
