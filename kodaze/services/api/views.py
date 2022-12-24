from rest_framework import status, generics, serializers, views
from rest_framework.response import Response
from services.api.serializers import (
    ServicePaymentSerializer,
    ServiceSerializer,
    ServiceProductForContractSerializer
)
from company.models import Company
from services.api import utils as service_utils
from services.api.services import service_model_services, service_product_for_contract_service
from services.api.selectors import service_list, service_payment_list, service_product_for_contract_list

from django_filters.rest_framework import DjangoFilterBackend

from services.api.filters import (
    ServiceFilter,
    ServicePaymentFilter,
    ServiceProductForContractFilter
)

from services.api import permissions as contract_permissions

# ********************************** service endpoints **********************************

class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = service_list()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter
    permission_classes = [contract_permissions.ServicePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(contract__company=request.user.company, contract__office=request.user.office)
            queryset = self.queryset.filter(contract__company=request.user.company)
        else:
            queryset = self.queryset
        
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        
        extra = dict()
        all_price = 0
        all_total_paid_amount = 0
        all_remaining_payment = 0
        for q in page:
            all_price += q.price
            all_total_paid_amount += q.total_paid_amount
            all_remaining_payment += q.remaining_payment
            
            extra['all_price'] = all_price
            extra['all_total_paid_amount'] = all_total_paid_amount
            extra['all_remaining_payment'] = all_remaining_payment

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'extra': extra, 'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=request.user
        service_model_services.service_create(user=user, **serializer.validated_data)
        return Response({'detail': 'Servis əlavə olundu'}, status=status.HTTP_201_CREATED)


class ServiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = service_list()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter
    permission_classes = [contract_permissions.ServicePermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        service_model_services.service_update(instance=instance, **serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** service odeme endpoints **********************************

class ServicePaymentListCreateAPIView(generics.ListCreateAPIView):
    queryset = service_payment_list()
    serializer_class = ServicePaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServicePaymentFilter
    permission_classes = [contract_permissions.ServicePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(service__contract__company=request.user.company, service__contract__office=request.user.office)
            queryset = self.queryset.filter(service__contract__company=request.user.company)
        else:
            queryset = self.queryset
        
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ServicePaymentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = service_payment_list()
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

class ServiceProductForContractOperation(views.APIView):
    class InputSerializer(serializers.Serializer):
        company = serializers.PrimaryKeyRelatedField(
            queryset=Company.objects.all(), required=True
        )
        product_and_period = serializers.CharField(required=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_product_for_contract_service.service_product_for_contract_operation(**serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'}, status=status.HTTP_200_OK)

class ServiceProductForContractListAPIView(generics.ListAPIView):
    queryset = service_product_for_contract_list()
    serializer_class = ServiceProductForContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceProductForContractFilter
    permission_classes = [contract_permissions.ServiceProductForContractPermissions]

class ServiceProductForContractRetriveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = service_product_for_contract_list()
    serializer_class = ServiceProductForContractSerializer
    permission_classes = [contract_permissions.ServiceProductForContractPermissions]