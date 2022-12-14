from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import generics
from product.api.serializers import (
    ProductSerializer,
    CategorySerializer,
    UnitOfMeasureSerializer
)

from django_filters.rest_framework import DjangoFilterBackend
from product.api.filters import (
    ProductFilter,
    CategoryFilter,
    UnitOfMeasureFilter,
)

from product.api.services import product_create, procut_update, product_delete
from product.api.selectors import unit_of_measure_list, category_list, product_list
from product.api import permissions as product_permissions
# ********************************** product put endpoints **********************************

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = product_list()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    permission_classes = [product_permissions.ProductPermissions]

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.all()        
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
    
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            product_create(**serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Məhsul əlavə edildi"}, status=status.HTTP_201_CREATED, headers=headers)

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = product_list()
    serializer_class = ProductSerializer
    permission_classes = [product_permissions.ProductPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            procut_update(instance, **serializer.validated_data)
        return Response({"detail": "Məhsul məlumatları yeniləndi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        product_delete(instance=instance)
        return Response({"detail": "Məhsul silindi"}, status=status.HTTP_204_NO_CONTENT)

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = category_list()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    permission_classes = [product_permissions.CategoryPermissions]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Kateqoriya əlavə edildi"}, status=status.HTTP_201_CREATED, headers=headers)


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = category_list()
    serializer_class = CategorySerializer
    permission_classes = [product_permissions.CategoryPermissions]

class UnitOfMeasureListCreateAPIView(generics.ListCreateAPIView):
    queryset = unit_of_measure_list()
    serializer_class = UnitOfMeasureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UnitOfMeasureFilter
    permission_classes = [product_permissions.UnitOfMeasurePermissions]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Ölçü vahidi əlavə edildi"}, status=status.HTTP_201_CREATED, headers=headers)


class UnitOfMeasureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = unit_of_measure_list()
    serializer_class = UnitOfMeasureSerializer
    permission_classes = [product_permissions.UnitOfMeasurePermissions]