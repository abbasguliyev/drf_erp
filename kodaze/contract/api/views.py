import datetime
import traceback

from django.shortcuts import get_object_or_404
from rest_framework import status, generics

import pandas as pd

from rest_framework.response import Response
from rest_framework import generics
from cashbox.models import OfficeCashbox

from rest_framework.decorators import api_view
from product.models import Product
from product.api.selectors import product_list


from contract.api.serializers import (
    DemoSalesSerializer,
    ContractChangeSerializer,
    ContractSerializer,
    ContractGiftSerializer,
    InstallmentSerializer,
    ContractCreditorSerializer
)

from contract.models import (
    ContractCreditor,
    ContractGift, 
    Contract, 
    Installment,  
    ContractChange, 
    DemoSales
)


from contract.api.utils import (
    installment_utils,
    contract_utils,
    contract_gift_utils,
)

from django_filters.rest_framework import DjangoFilterBackend

from contract.api.filters import (
    DemoSalesFilter,
    ContractGiftFilter,
    InstallmentFilter,
    ContractFilter,
)

from contract.api.services import contract_service, installment_service, contract_change_service

from contract.api import permissions as contract_permissions
 
# ********************************** contract endpoints **********************************

class ContractListCreateAPIView(generics.ListCreateAPIView):
    queryset = Contract.objects.select_related(
                    'group_leader', 
                    'manager1', 
                    'manager2', 
                    'customer', 
                    'product', 
                    'company', 
                    'office', 
                ).all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilter
    permission_classes = [contract_permissions.ContractPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(company=request.user.company, office=request.user.office)
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
        return contract_service.contract_create(self, request, *args, **kwargs)


class ContractDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Contract.objects.select_related(
                    'group_leader', 
                    'manager1', 
                    'manager2', 
                    'customer', 
                    'product', 
                    'company', 
                    'office', 
                ).all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilter
    permission_classes = [contract_permissions.ContractPermissions]

    def update(self, request, *args, **kwargs):
        return contract_service.contract_update(self, request, *args, **kwargs)


# ********************************** odeme tarixi put endpoints **********************************


class InstallmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Installment.objects.select_related('contract').all()
    serializer_class = InstallmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = InstallmentFilter
    permission_classes = [contract_permissions.InstallmentleriPermissions]

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
        total_price = 0
        total_remaining_debt = 0

        for q in page:
            total_price += q.price
            extra['total_price'] = total_price

        unique_contracts = set(d.contract for d in page)
        for unique_contract in unique_contracts:
            total_remaining_debt += unique_contract.remaining_debt
            extra['total_remaining_debt'] = total_remaining_debt

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'extra': extra, 'data':serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response([
                {'extra': extra, 'data':serializer.data}
            ])

    # def create(self, request, *args, **kwargs):
    #     return contract_utils.contract_create(self, request, *args, **kwargs)

class InstallmentDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contract']
    filterset_class = InstallmentFilter
    permission_classes = [contract_permissions.InstallmentleriPermissions]

    # PUT SORGUSU
    def update(self, request, *args, **kwargs):
        return installment_service.installment_update(self, request, *args, **kwargs)


# ********************************** hediyye endpoints **********************************
class ContractGiftListCreateAPIView(generics.ListCreateAPIView):
    queryset = ContractGift.objects.select_related('contract', 'product').all()
    serializer_class = ContractGiftSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractGiftFilter
    permission_classes = [contract_permissions.ContractGiftPermissions]

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
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return contract_gift_utils.gifts_create(self, request, *args, **kwargs)


class ContractGiftDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = ContractGift.objects.select_related('contract', 'product').all()
    serializer_class = ContractGiftSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractGiftFilter
    permission_classes = [contract_permissions.ContractGiftPermissions]

    def destroy(self, request, *args, **kwargs):
        return contract_gift_utils.gifts_destroy(self, request, *args, **kwargs)

# ********************************** ContractChange endpoints **********************************

class ContractChangeListCreateAPIView(generics.ListCreateAPIView):
    queryset = ContractChange.objects.all()
    serializer_class = ContractChangeSerializer
    permission_classes = [contract_permissions.ContractChangePermissions]

    def create(self, request, *args, **kwargs):
        return contract_change_service.contract_change(self, request, *args, **kwargs)
# ********************************** demo sale endpoints **********************************

class DemoSalesListAPIView(generics.ListAPIView):
    queryset = DemoSales.objects.all()
    serializer_class = DemoSalesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DemoSalesFilter
    permission_classes = [contract_permissions.DemoSalesPermissions]


class DemoSalesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DemoSales.objects.all()
    serializer_class = DemoSalesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DemoSalesFilter
    permission_classes = [contract_permissions.DemoSalesPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            count_q = serializer.validated_data.get("count")
            count = instance.count + count_q
            serializer.save(count=count)
            return Response({"detail": "Demo əlavə olundu"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_test_installment(request):
    """
    Contract imzalanmadan aylara dusen meblegi gormek ucun funksiya

    request = {
        "loan_term":10,
        "product_quantity":10,
        "payment_style":"KREDİT",
        "contract_date":"2022-07-28",
        "initial_payment":100,
        "initial_payment_debt":0,
        "product_id":1,
        "loan_term":10
    }
    """
    instance = request
    loan_term = instance.data.get("loan_term")
    product_quantity = instance.data.get("product_quantity")
    product_id = instance.data.get("product_id")
    payment_style = instance.data.get("payment_style")
    product = product_list().filter(pk=product_id).last()
    contract_date_str = instance.data.get("contract_date")
    contract_date = datetime.datetime.strptime(contract_date_str, '%d-%m-%Y')

    initial_payment = instance.data.get("initial_payment")
    initial_payment_debt = instance.data.get("initial_payment_debt")

    umumi_installment = []

    if(payment_style == "KREDİT"):
        now = contract_date
        inc_month = pd.date_range(now, periods = loan_term+1, freq='M')
        initial_payment = initial_payment
        initial_payment_debt = initial_payment_debt

        if(initial_payment is not None):
            initial_payment = initial_payment
        
        if(initial_payment_debt is not None):
            initial_payment_debt = initial_payment_debt

        productun_pricei = product_quantity * product.price
        if(initial_payment_debt == 0):
            initial_payment_tam = initial_payment
        elif(initial_payment_debt != 0):
            initial_payment_tam = initial_payment + initial_payment_debt
        aylara_gore_odenecek_umumi_amount = productun_pricei - initial_payment_tam
        
        if(loan_term > 0):
            aylara_gore_odenecek_amount = aylara_gore_odenecek_umumi_amount // loan_term

            qaliq = aylara_gore_odenecek_amount * (loan_term - 1)
            son_aya_odenecek_amount = aylara_gore_odenecek_umumi_amount - qaliq

            i = 1
            while(i<=loan_term):
                if(i == loan_term):
                    if(now.day < 29):
                        installment = {}
                        installment["month_no"] = i
                        installment["date"] = f"{inc_month[i].year}-{inc_month[i].month}-{now.day}"
                        installment["price"] = son_aya_odenecek_amount
                        umumi_installment.append(installment)
                    elif(now.day == 31 or now.day == 30 or now.day == 29):
                        if(inc_month[i].day <= now.day):
                            installment = {}
                            installment["month_no"] = i
                            installment["date"] = f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}"
                            installment["price"] = son_aya_odenecek_amount
                            umumi_installment.append(installment)
                            
                        elif(inc_month[i].day > now.day):
                            installment = {}
                            installment["month_no"] = i
                            installment["date"] = f"{inc_month[i].year}-{inc_month[i].month}-{now.day}"
                            installment["price"] = son_aya_odenecek_amount
                            umumi_installment.append(installment)
                else:
                    if(now.day < 29):
                        installment = {}
                        installment["month_no"] = i
                        installment["date"] = f"{inc_month[i].year}-{inc_month[i].month}-{now.day}"
                        installment["price"] = aylara_gore_odenecek_amount
                        umumi_installment.append(installment)
                        
                    elif(now.day == 31 or now.day == 30 or now.day == 29):
                        if(inc_month[i].day <= now.day):
                            installment = {}
                            installment["month_no"] = i
                            installment["date"] = f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}"
                            installment["price"] = aylara_gore_odenecek_amount
                            umumi_installment.append(installment)
                            
                        if(inc_month[i].day > now.day):
                            installment = {}
                            installment["month_no"] = i
                            installment["date"] = f"{inc_month[i].year}-{inc_month[i].month}-{now.day}"
                            installment["price"] = aylara_gore_odenecek_amount
                            umumi_installment.append(installment)
                i+=1
    return Response(umumi_installment)


class ContractCreditorListCreateAPIView(generics.ListCreateAPIView):
    queryset = ContractCreditor.objects.all()
    serializer_class = ContractCreditorSerializer
    permission_classes = [contract_permissions.ContractCreditorPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = ContractCreditor.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = ContractCreditor.objects.filter(contract__company=request.user.company, contract__office=request.user.office)
            queryset = ContractCreditor.objects.filter(contract__company=request.user.company)
        else:
            queryset = ContractCreditor.objects.all()
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
            contract = serializer.validated_data.get("contract")
            creditor_contracts = ContractCreditor.objects.filter(contract=contract)
            if len(creditor_contracts)>0:
                return Response({"detail":"Bir müqaviləyə birdən artıq creditor təyin edilə bilməz"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"detail":"Müqavilə creditor əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

class ContractCreditorDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = ContractCreditor.objects.all()
    serializer_class = ContractCreditorSerializer
    permission_classes = [contract_permissions.ContractCreditorPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"Müqavilə creditor məlumatları yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)
