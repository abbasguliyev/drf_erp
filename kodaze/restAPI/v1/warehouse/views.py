import datetime
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import generics

from restAPI.v1.warehouse.serializers import (
    WarehouseSerializer,
    OperationSerializer,
    WarehouseRequestSerializer,
    StockSerializer,
)

from warehouse.models import (
    Operation,
    Warehouse,
    WarehouseRequest,
    Stock
)
from restAPI.v1.warehouse.utils import (
    warehouse_operation_utils,
    stok_utils
)

from django_filters.rest_framework import DjangoFilterBackend

from restAPI.v1.warehouse.filters import (
    WarehouseFilter,
    WarehouseRequestFilter,
    OperationFilter,
    StockFilter,
)

from restAPI.v1.warehouse import permissions as contract_permissions

# ********************************** warehouse put get post delete **********************************


class WarehouseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseFilter
    permission_classes = [contract_permissions.WarehousePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Warehouse.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = Warehouse.objects.filter(
                    company=request.user.company, office=request.user.office)
            queryset = Warehouse.objects.filter(company=request.user.company)
        else:
            queryset = Warehouse.objects.all()

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
            office = serializer.validated_data.get("office")
            is_have_warehouse = Warehouse.objects.filter(office=office)
            if len(is_have_warehouse) > 0:
                return Response({"detail": "Bir officein yalnız bir warehouseı ola bilər!"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"detail": "Warehouse quruldu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)


class WarehouseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseFilter
    permission_classes = [contract_permissions.WarehousePermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Warehouse məlumatları yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Məlumatları doğru daxil edin."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        warehouse = self.get_object()
        warehouse.is_active = False
        warehouse.save()
        return Response({"detail": "Warehouse qeyri-atkiv edildi"}, status=status.HTTP_200_OK)

# ********************************** warehouse put delete post get **********************************


class WarehouseRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = WarehouseRequest.objects.all()
    serializer_class = WarehouseRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseRequestFilter
    permission_classes = [contract_permissions.WarehouseRequestPermissions]

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
    permission_classes = [contract_permissions.WarehouseRequestPermissions]

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

# ********************************** operation put delete post get **********************************


class OperationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OperationFilter
    permission_classes = [contract_permissions.OperationPermissions]

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
    permission_classes = [contract_permissions.OperationPermissions]

    def update(self, request, *args, **kwargs):
        return warehouse_operation_utils.operation_create(self, request, *args, **kwargs)

# ********************************** stok put delete post get **********************************


class StockListCreateAPIView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockFilter
    permission_classes = [contract_permissions.StockPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Stock.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = Stock.objects.filter(
                    warehouse__company=request.user.company, warehouse__office=request.user.office)
            queryset = Stock.objects.filter(warehouse__company=request.user.company)
        else:
            queryset = Stock.objects.all()

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
            executor = request.user
            warehouse = serializer.validated_data.get("warehouse")
            product = serializer.validated_data.get("product")
            note = serializer.validated_data.get("note")
            date = datetime.date.today()
            stok = Stock.objects.filter(warehouse=warehouse, product=product)
            quantity = serializer.validated_data.get("quantity")
            if len(stok) > 0:
                return Response({"detail": "Bu adlı stok artıq var. Yenisini əlavə edə bilməzsiniz"}, status=status.HTTP_400_BAD_REQUEST)
            operation = Operation.objects.create(
                executor=executor,
                quantity=abs(quantity),
                operation_type="stok yeniləmə",
                operation_date=date,
                note=note,
                shipping_warehouse=None,
                receiving_warehouse=None,
                product_and_quantity=product.product_name
            )
            operation.save()
            serializer.save()
            return Response({"detail": "Stock əlavə edildi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)


class StockDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockFilter
    permission_classes = [contract_permissions.StockPermissions]

    def update(self, request, *args, **kwargs):
        return stok_utils.stok_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)
