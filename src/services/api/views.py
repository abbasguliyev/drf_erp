import datetime
from rest_framework import status, generics, serializers, views
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django_filters.rest_framework import DjangoFilterBackend
from company.api.selectors import company_list
from company.models import Company
from services.api.serializers import (
    ServicePaymentSerializer,
    ServiceSerializer,
    ServiceProductForContractSerializer
)
from services.api.services import service_model_services, service_product_for_contract_service, service_payment_services
from services.api.selectors import service_list, service_payment_list, service_product_for_contract_list

from services.api.filters import (
    ServiceFilter,
    ServicePaymentFilter,
    ServiceProductForContractFilter
)
from services.api import permissions as service_permissions

# ********************************** service endpoints **********************************

class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = service_list()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter
    permission_classes = [service_permissions.ServicePermissions]

    def get(self, request, *args, **kwargs):
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
            
            extra['all_price'] = int(all_price)
            extra['all_total_paid_amount'] = int(all_total_paid_amount)
            extra['all_remaining_payment'] = int(all_remaining_payment)

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
    permission_classes = [service_permissions.ServicePermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = request.user
        service_model_services.service_update(user=user, instance=instance, **serializer.validated_data)
        return Response({'detail': 'Əməliyyat yerinə yetirildi'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

# ********************************** service odeme endpoints **********************************

class ServicePaymentListAPIView(generics.ListAPIView):
    queryset = service_payment_list()
    serializer_class = ServicePaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServicePaymentFilter
    permission_classes = [service_permissions.ServicePermissions]

    def get(self, request, *args, **kwargs):
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
    permission_classes = [service_permissions.ServicePermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = request.user
        service_payment_services.service_payment_update(instance=instance, user=user, **serializer.validated_data)
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)

class ServiceProductForContractOperation(views.APIView):
    permission_classes = [service_permissions.ServiceProductForContractPermissions]

    class InputSerializer(serializers.Serializer):
        company = serializers.PrimaryKeyRelatedField(
            queryset=company_list(), required=True
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
    permission_classes = [service_permissions.ServiceProductForContractPermissions]

class ServiceProductForContractRetriveDestroyAPIView(generics.RetrieveAPIView):
    queryset = service_product_for_contract_list()
    serializer_class = ServiceProductForContractSerializer
    permission_classes = [service_permissions.ServiceProductForContractPermissions]


@api_view(['POST'])
def create_test_installment_service(request):
    """
    Servis imzalanmadan aylara dusen meblegi gormek ucun funksiya

    request = {
        "product":[1],
        "product_quantity": "1",
        "start_date_of_payment":"2022-07-28",
        "loan_term":10,
        "initial_payment":100,
        "discount":0
    }
    """
    product = request.data.get('product')
    product_quantity = request.data.get('product_quantity')
    start_date_of_payment = request.data.get('start_date_of_payment')
    loan_term = request.data.get('loan_term')
    initial_payment = request.data.get('initial_payment')
    discount = request.data.get('discount')

    test_service_payments = service_payment_services.test_installment_service_create(
        product=product,
        product_quantity=product_quantity,
        start_date_of_payment=start_date_of_payment,
        loan_term=loan_term, initial_payment=initial_payment,
        discount=discount
    )
    
    return Response(test_service_payments)