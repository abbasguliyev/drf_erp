from rest_framework import status, generics
from rest_framework.response import Response
from restAPI.v1.services.serializers import (
    ServicePaymentSerializer,
    ServiceSerializer,
)

from services.models import (
    Service,
    ServicePayment, 
)
from restAPI.v1.services import utils as service_utils

from django_filters.rest_framework import DjangoFilterBackend

from restAPI.v1.services.filters import (
    ServiceFilter,
    ServicePaymentFilter,
)

from restAPI.v1.services import permissions as contract_permissions

# ********************************** service put delete post get **********************************

class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter
    permission_classes = [contract_permissions.ServicePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Service.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = Service.objects.filter(contract__company=request.user.company, contract__office=request.user.office)
            queryset = Service.objects.filter(contract__company=request.user.company)
        else:
            queryset = Service.objects.all()
        
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return service_utils.service_create(self, request, *args, **kwargs)


class ServiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter
    permission_classes = [contract_permissions.ServicePermissions]

    def update(self, request, *args, **kwargs):
        return service_utils.service_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** service odeme put delete post get **********************************

class ServicePaymentListCreateAPIView(generics.ListCreateAPIView):
    queryset = ServicePayment.objects.all()
    serializer_class = ServicePaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServicePaymentFilter
    permission_classes = [contract_permissions.ServicePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = ServicePayment.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = ServicePayment.objects.filter(service__contract__company=request.user.company, service__contract__office=request.user.office)
            queryset = ServicePayment.objects.filter(service__contract__company=request.user.company)
        else:
            queryset = ServicePayment.objects.all()
        
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ServicePaymentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServicePayment.objects.all()
    serializer_class = ServicePaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServicePaymentFilter
    permission_classes = [contract_permissions.ServicePermissions]

    def update(self, request, *args, **kwargs):
        return service_utils.service_payment_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)
