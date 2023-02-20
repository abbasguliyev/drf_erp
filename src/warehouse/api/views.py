from rest_framework import status, generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.validators import UniqueTogetherValidator

from django_filters.rest_framework import DjangoFilterBackend

from warehouse.api.serializers import (
    WarehouseSerializer,
    WarehouseRequestSerializer,
    StockSerializer,
    ChangeUnuselessOperationSerializer,
    HoldingWarehouseSerializer,
    WarehouseHistorySerializer
)

from warehouse.api.filters import (
    WarehouseFilter,
    WarehouseRequestFilter,
    StockFilter,
    HoldingWarehouseFilter,
    WarehouseHistoryFilter
)

from warehouse.api import permissions as warehouse_permissions
from warehouse.api.selectors import (
    holding_warehouse_list,
    warehouse_list,
    stock_list,
    warehouse_request_list,
    warehouse_history_list
)
from warehouse.api.services.warehouse_request_service import warehouse_request_create, warehouse_request_execute
from warehouse.api.services.warehouse_service import warehouse_update, warehouse_delete, \
    product_add_to_holding_warehouse, holding_warehouse_update
from warehouse.api.services.product_transfer_service import (
    holding_office_product_transfer_service,
    between_office_product_transfer_service,
    office_to_holding_product_transfer
)
from warehouse.api.services.change_unuseless_service import change_unuseless_operation_create
from product.api.selectors import category_list, unit_of_measure_list, product_list
from company.models import Company, Office
from company.api.selectors import company_list, office_list


# ********************************** warehouse endpoints **********************************


class WarehouseListAPIView(generics.ListAPIView):
    queryset = warehouse_list()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseFilter
    permission_classes = [warehouse_permissions.WarehousePermissions]

    def get(self, request, *args, **kwargs):
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
    queryset = warehouse_request_list()
    serializer_class = WarehouseRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseRequestFilter
    permission_classes = [warehouse_permissions.WarehouseRequestPermissions]

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
        user = request.user
        if serializer.is_valid():
            warehouse_request_create(user=user, **serializer.validated_data)
            return Response({"detail": "Sorğu göndərildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class WarehouseRequestRetriveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = warehouse_request_list()
    serializer_class = WarehouseRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseRequestFilter
    permission_classes = [warehouse_permissions.WarehouseRequestPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)


class WarehouseRequestExecuteAPIView(APIView):
    permission_classes = [warehouse_permissions.WarehouseRequestPermissions]

    class InputSerializer(serializers.Serializer):
        products_and_quantity = serializers.CharField(required=False)
        company = serializers.PrimaryKeyRelatedField(queryset=company_list(), required=False)
        office = serializers.PrimaryKeyRelatedField(queryset=office_list(), required=False)
        note = serializers.CharField(required=False)
        status = serializers.CharField(required=True)

    def post(self, request, pk):
        serializer = self.InputSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            warehouse_request_execute(instance_id=pk, user=user, **serializer.validated_data)
            return Response({'detail': 'Əməliyyatı yerinə yetirildi'}, status=status.HTTP_200_OK)
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# ********************************** stok endpoints **********************************

class StockListCreateAPIView(generics.ListAPIView):
    queryset = stock_list()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockFilter
    permission_classes = [warehouse_permissions.StockPermissions]

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)

        extra = dict()
        all_quantity = 0
        all_useful_product_count = 0
        all_changed_product_count = 0
        for q in page:
            all_quantity += q.quantity
            all_useful_product_count += q.useful_product_count
            all_changed_product_count += q.changed_product_count

            extra['all_quantity'] = int(all_quantity)
            extra['all_useful_product_count'] = int(all_useful_product_count)
            extra['all_changed_product_count'] = int(all_changed_product_count)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'extra': extra, 'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# ********************************** product transfer endpoints **********************************

class HoldingToOfficeProductTransfer(APIView):
    permission_classes = [warehouse_permissions.StockPermissions]

    class InputSerializer(serializers.Serializer):
        products_and_quantity = serializers.CharField()
        company = serializers.PrimaryKeyRelatedField(queryset=company_list(), required=True)
        warehouse = serializers.PrimaryKeyRelatedField(queryset=office_list(), required=True)
        note = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        holding_office_product_transfer_service(user=user, **serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_200_OK)


class BetweenOfficeProductTransfer(APIView):
    permission_classes = [warehouse_permissions.StockPermissions]

    class InputSerializer(serializers.Serializer):
        products_and_quantity = serializers.CharField()
        company = serializers.PrimaryKeyRelatedField(queryset=company_list(), required=True)
        sender_office = serializers.PrimaryKeyRelatedField(queryset=office_list(), required=True)
        recipient_office = serializers.PrimaryKeyRelatedField(queryset=office_list(), required=True)
        note = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        between_office_product_transfer_service(user=user, **serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_200_OK)


class OfficeToHoldingProductTransfer(APIView):
    permission_classes = [warehouse_permissions.StockPermissions]

    class InputSerializer(serializers.Serializer):
        products_and_quantity = serializers.CharField()
        company = serializers.PrimaryKeyRelatedField(queryset=company_list(), required=True)
        warehouse = serializers.PrimaryKeyRelatedField(queryset=office_list(), required=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        office_to_holding_product_transfer(user=user, **serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_200_OK)


class ChangeUnuselessOperationAPIView(APIView):
    permission_classes = [warehouse_permissions.ChangeUnuselessOperationPermissions]

    def post(self, request):
        serializer = ChangeUnuselessOperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        change_unuseless_operation_create(user=user, **serializer.validated_data)
        return Response({'detail': 'Utilizasiya prosesi yerinə yetirildi'}, status=status.HTTP_200_OK)


class HoldingWarehouseAPIView(generics.ListAPIView):
    queryset = holding_warehouse_list()
    serializer_class = HoldingWarehouseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HoldingWarehouseFilter
    permission_classes = [warehouse_permissions.HoldingWarehousePermissions]

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        extra = dict()
        all_quantity = 0
        all_useful_product_count = 0
        all_unuseful_product_count = 0
        all_price = 0
        for q in page:
            all_quantity += q.quantity
            all_useful_product_count += q.useful_product_count
            all_unuseful_product_count += q.unuseful_product_count
            all_price += q.product.price

            extra['all_quantity'] = int(all_quantity)
            extra['all_useful_product_count'] = int(all_useful_product_count)
            extra['all_unuseful_product_count'] = int(all_unuseful_product_count)
            extra['all_price'] = int(all_price)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'extra': extra, 'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HoldingWarehouseRetriveAPIView(generics.RetrieveAPIView):
    queryset = holding_warehouse_list()
    serializer_class = HoldingWarehouseSerializer
    permission_classes = [warehouse_permissions.HoldingWarehousePermissions]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class HoldingWarehouseDestroyAPIView(generics.DestroyAPIView):
    queryset = holding_warehouse_list()
    serializer_class = HoldingWarehouseSerializer
    permission_classes = [warehouse_permissions.HoldingWarehousePermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.useful_product_count > 0:
            return Response({'detail': 'Silmə əməliyyatı yalnız sayı 0 olan məhsullar üçün keçərlidir'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            instance.delete()
            return Response({'detail': 'Məhsul Holdinq anbardan silindi'}, status=status.HTTP_204_NO_CONTENT)


class HoldingWarehouseUpdateAPIView(APIView):
    permission_classes = [warehouse_permissions.HoldingWarehousePermissions]

    class InputSerializer(serializers.Serializer):
        product_name = serializers.CharField(required=False)
        barcode = serializers.IntegerField(required=False)
        category = serializers.PrimaryKeyRelatedField(queryset=category_list(), required=False)
        unit_of_measure = serializers.PrimaryKeyRelatedField(queryset=unit_of_measure_list(), required=False)
        purchase_price = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        price = serializers.DecimalField(max_digits=20, decimal_places=0, required=False)
        guarantee = serializers.IntegerField(required=False)
        is_gift = serializers.BooleanField(required=False)
        weight = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        width = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        length = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        height = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        volume = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        note = serializers.CharField(required=False)
        product_image = serializers.ImageField(required=False)
        quantity = serializers.IntegerField(required=False)

    def put(self, request, pk):
        serializer = self.InputSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user = request.user
            holding_warehouse_update(user=user, instance=pk, **serializer.validated_data)
            return Response({'detail': 'Əməliyyatı yerinə yetirildi'}, status=status.HTTP_200_OK)
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProductAddToHoldigWarehouseAPIView(APIView):
    permission_classes = [warehouse_permissions.HoldingWarehousePermissions]
    
    class InputSerializer(serializers.Serializer):
        product_name = serializers.CharField(required=True)
        barcode = serializers.IntegerField(required=False, allow_null=True, )
        category = serializers.PrimaryKeyRelatedField(queryset=category_list(), write_only=True, required=False,
                                                      allow_null=True)
        unit_of_measure = serializers.PrimaryKeyRelatedField(queryset=unit_of_measure_list(), write_only=True,
                                                             required=False, allow_null=True)
        purchase_price = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        price = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        guarantee = serializers.IntegerField(required=False, allow_null=True)
        is_gift = serializers.BooleanField(required=False, allow_null=True)
        weight = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        width = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        length = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        height = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        volume = serializers.DecimalField(max_digits=20, decimal_places=0, required=False, allow_null=True)
        note = serializers.CharField(required=False, allow_null=True)
        product_image = serializers.ImageField(required=False, allow_null=True)
        quantity = serializers.IntegerField(required=False, allow_null=True)
        useful_product_count = serializers.IntegerField(required=False, allow_null=True)
        unuseful_product_count = serializers.IntegerField(required=False, allow_null=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        product_add_to_holding_warehouse(user=user, **serializer.validated_data)
        return Response({'detail': 'Əməliyyatı yerinə yetirildi'}, status=status.HTTP_200_OK)


class WarehouseHistoryListAPIView(generics.ListAPIView):
    queryset = warehouse_history_list()
    serializer_class = WarehouseHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseHistoryFilter
    permission_classes = [warehouse_permissions.WarehouseHistoryPermissions]


class GetAllWarehouse(APIView):
    def get(self, request):
        w_l = list()
        warehouses = warehouse_list()
        for w in warehouses:
            w_d_2 = dict()
            w_d_2['name'] = w.name
            w_d_2['company'] = w.office.company.name
            w_l.append(w_d_2)

        w_d = dict()
        holding_warehouse = "Holding anbarı"
        w_d['name'] = holding_warehouse
        w_d['company'] = None

        w_l.append(w_d)

        return Response(w_l)
