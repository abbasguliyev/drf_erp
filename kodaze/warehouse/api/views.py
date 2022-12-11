from rest_framework import status, generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.validators import UniqueTogetherValidator

from django_filters.rest_framework import DjangoFilterBackend

from warehouse.api.serializers import (
    WarehouseSerializer,
    OperationSerializer,
    WarehouseRequestSerializer,
    StockSerializer,
    ChangeUnuselessOperationSerializer,
    HoldingWarehouseSerializer
)

from warehouse.models import (
    Operation,
    WarehouseRequest,
)
from warehouse.api.utils import warehouse_operation_utils

from warehouse.api.filters import (
    WarehouseFilter,
    WarehouseRequestFilter,
    OperationFilter,
    StockFilter,
    HoldingWarehouseFilter
)

from warehouse.api import permissions as warehouse_permissions
from warehouse.api.selectors import (
    holding_warehouse_list, 
    warehouse_list, 
    stock_list, 
    change_unuseless_operation_list
)
from warehouse.api.services.warehouse_service import warehouse_update, warehouse_delete, product_add_to_holding_warehouse
from warehouse.api.services.product_transfer_service import (
    holding_office_product_transfer_service,

)
from warehouse.api.services.change_unuseless_service import change_unuseless_operation_create
from product.api.selectors import category_list, unit_of_measure_list, product_list
from company.models import Company, Office

# ********************************** warehouse endpoints **********************************


class WarehouseListAPIView(generics.ListAPIView):
    queryset = warehouse_list()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseFilter
    permission_classes = [warehouse_permissions.WarehousePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(
                    company=request.user.company, office=request.user.office)
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


class WarehouseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = warehouse_list()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseFilter
    permission_classes = [warehouse_permissions.WarehousePermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            warehouse_update(instance, **serializer.validated_data)
            return Response({"detail": "Anbar məlumatları yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        warehouse_delete(instance=instance)
        return Response({"detail": "Anbar qeyri-atkiv edildi"}, status=status.HTTP_200_OK)

# ********************************** warehouse request endpoints **********************************


class WarehouseRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = WarehouseRequest.objects.all()
    serializer_class = WarehouseRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseRequestFilter
    permission_classes = [warehouse_permissions.WarehouseRequestPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = WarehouseRequest.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = WarehouseRequest.objects.filter(
                    warehouse__company=request.user.company, warehouse__office=request.user.office)
            queryset = WarehouseRequest.objects.filter(
                warehouse__company=request.user.company)
        else:
            queryset = WarehouseRequest.objects.all()

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
            serializer.save(employee_who_sent_the_request=user)
            return Response({"detail": "Sorğu göndərildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Məlumatları doğru daxil edin."}, status=status.HTTP_400_BAD_REQUEST)


class WarehouseRequestDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WarehouseRequest.objects.all()
    serializer_class = WarehouseRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseRequestFilter
    permission_classes = [warehouse_permissions.WarehouseRequestPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Sorğu yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Məlumatları doğru daxil edin."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)


# ********************************** stok endpoints **********************************

class StockListCreateAPIView(generics.ListAPIView):
    queryset = stock_list()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockFilter
    permission_classes = [warehouse_permissions.StockPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(
                    warehouse__company=request.user.company, warehouse__office=request.user.office)
            queryset = self.queryset.filter(
                warehouse__company=request.user.company)
        else:
            queryset = self.queryset

        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# ********************************** product transfer endpoints **********************************

class HoldingOfficeProductTransfer(APIView):
    class InputSerializer(serializers.Serializer):
        products_and_quantity = serializers.CharField()
        company = serializers.PrimaryKeyRelatedField(
            queryset=Company.objects.all(), required=True)
        warehouse = serializers.PrimaryKeyRelatedField(
            queryset=Office.objects.all(), required=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        holding_office_product_transfer_service(**serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_200_OK)

class BetweenOfficeProductTransfer(APIView):
    class InputSerializer(serializers.Serializer):
        products_and_quantity = serializers.CharField()
        company = serializers.PrimaryKeyRelatedField(
            queryset=Company.objects.all(), required=True)
        sender_office = serializers.PrimaryKeyRelatedField(
            queryset=Office.objects.all(), required=True)
        recipient_office = serializers.PrimaryKeyRelatedField(
            queryset=Office.objects.all(), required=True)


    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        holding_office_product_transfer_service(**serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_200_OK)


# ********************************** operation endpoints **********************************


class OperationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OperationFilter
    permission_classes = [warehouse_permissions.OperationPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Operation.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = Operation.objects.filter(shipping_warehouse__company=request.user.company, shipping_warehouse__office=request.user.office,
                                                    receiving_warehouse__company=request.user.company, receiving_warehouse__office=request.user.office)
            queryset = Operation.objects.filter(
                shipping_warehouse__company=request.user.company, receiving_warehouse__company=request.user.company)
        else:
            queryset = Operation.objects.all()

        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return warehouse_operation_utils.operation_create(self, request, *args, **kwargs)


class OperationDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OperationFilter
    permission_classes = [warehouse_permissions.OperationPermissions]

    def update(self, request, *args, **kwargs):
        return warehouse_operation_utils.operation_create(self, request, *args, **kwargs)


class ChangeUnuselessOperationAPIView(APIView):
    def post(self, request):
        serializer = ChangeUnuselessOperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        change_unuseless_operation_create(**serializer.validated_data)
        return Response({'detail': 'Utilizasiya prosesi yerinə yetirildi'}, status=status.HTTP_200_OK)


class HoldingWarehouseAPIView(generics.ListAPIView):
    queryset = holding_warehouse_list()
    serializer_class = HoldingWarehouseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingWarehouseFilter
    permission_classes = [warehouse_permissions.HoldingWarehousePermissions]


class ProductAddToHoldigWarehouseAPIView(APIView):
    class InputSerializer(serializers.Serializer):
        product_name = serializers.CharField(required=True)
        barcode = serializers.IntegerField(required=False, allow_null=True,)
        category = serializers.PrimaryKeyRelatedField(queryset=category_list(), write_only=True, required=False, allow_null=True)
        unit_of_measure = serializers.PrimaryKeyRelatedField(queryset=unit_of_measure_list(), write_only=True, required=False, allow_null=True)
        purchase_price = serializers.FloatField(required=False, allow_null=True)
        price = serializers.DecimalField(max_digits=20, decimal_places=2, required=False, allow_null=True)
        guarantee = serializers.IntegerField(required=False, allow_null=True)
        is_gift = serializers.BooleanField(required=False, allow_null=True)
        weight = serializers.FloatField(required=False, allow_null=True)
        width = serializers.FloatField(required=False, allow_null=True)
        length = serializers.FloatField(required=False, allow_null=True)
        height = serializers.FloatField(required=False, allow_null=True)
        volume = serializers.FloatField(required=False, allow_null=True)
        note = serializers.CharField(required=False, allow_null=True)
        product_image = serializers.ImageField(required=False, allow_null=True)
        quantity = serializers.IntegerField(required=False, allow_null=True)
        useful_product_count = serializers.IntegerField(required=False, allow_null=True)
        unuseful_product_count = serializers.IntegerField(required=False, allow_null=True)

        class Meta:
            validators = [
            UniqueTogetherValidator(
                queryset=product_list(),
                fields=['barcode']
            )
        ]

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_add_to_holding_warehouse(**serializer.validated_data)
        return Response({'detail': 'Əməliyyatı yerinə yetirildi'}, status=status.HTTP_200_OK)
