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
from warehouse.models import Stock, Warehouse

from restAPI.v1.contract.serializers import (
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


from restAPI.v1.contract.utils import (
    installment_utils,
    contract_utils,
    contract_gift_utils,
)

from django_filters.rest_framework import DjangoFilterBackend

from restAPI.v1.contract.filters import (
    DemoSalesFilter,
    ContractGiftFilter,
    InstallmentFilter,
    ContractFilter,
)

from restAPI.v1.contract import permissions as contract_permissions
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
 
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
# ********************************** contract get post put delete **********************************

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
            queryset = Contract.objects.select_related(
                    'group_leader', 
                    'manager1', 
                    'manager2', 
                    'customer', 
                    'product', 
                    'company', 
                    'office', 
                ).all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = Contract.objects.select_related(
                    'group_leader', 
                    'manager1', 
                    'manager2', 
                    'customer', 
                    'product', 
                    'company', 
                    'office', 
                ).filter(company=request.user.company, office=request.user.office)
            queryset = Contract.objects.select_related(
                    'group_leader', 
                    'manager1', 
                    'manager2', 
                    'customer', 
                    'product', 
                    'company', 
                    'office', 
                ).filter(company=request.user.company)
        else:
            queryset = Contract.objects.all()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return contract_utils.contract_create(self, request, *args, **kwargs)


class ContractDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilter
    permission_classes = [contract_permissions.ContractPermissions]

    def patch(self, request, *args, **kwargs):
        return contract_utils.contract_patch(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return contract_utils.contract_update(self, request, *args, **kwargs)


# ********************************** odeme datei put get post delete **********************************


class InstallmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = InstallmentFilter
    permission_classes = [contract_permissions.InstallmentleriPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Installment.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = Installment.objects.filter(contract__company=request.user.company, contract__office=request.user.office)
            queryset = Installment.objects.filter(contract__company=request.user.company)
        else:
            queryset = Installment.objects.all()
        
        queryset = self.filter_queryset(queryset)

        umumi_quantity = 0

        for q in queryset:
            umumi_quantity += q.price

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'umumi_quantity': umumi_quantity, 'data':serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response([
                {'umumi_quantity': umumi_quantity, 'data':serializer.data}
            ])

    def create(self, request, *args, **kwargs):
        return contract_utils.contract_create(self, request, *args, **kwargs)

class InstallmentDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contract']
    filterset_class = InstallmentFilter
    permission_classes = [contract_permissions.InstallmentleriPermissions]

    # # PATCH SORGUSU
    # def patch(self, request, *args, **kwargs):
    #     return payment_dateleri_utils.installment_patch(self, request, *args, **kwargs)

    # PUT SORGUSU
    def update(self, request, *args, **kwargs):
        return payment_dateleri_utils.installment_update(self, request, *args, **kwargs)


# ********************************** hediyye put delete post get **********************************
class ContractGiftListCreateAPIView(generics.ListCreateAPIView):
    queryset = ContractGift.objects.all()
    serializer_class = ContractGiftSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractGiftFilter
    permission_classes = [contract_permissions.ContractGiftPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = ContractGift.objects.all()
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = ContractGift.objects.filter(contract__company=request.user.company, contract__office=request.user.office)
            queryset = ContractGift.objects.filter(contract__company=request.user.company)
        else:
            queryset = ContractGift.objects.all()
        
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return gifts_utils.gifts_create(self, request, *args, **kwargs)


class ContractGiftDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = ContractGift.objects.all()
    serializer_class = ContractGiftSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractGiftFilter
    permission_classes = [contract_permissions.ContractGiftPermissions]

    def destroy(self, request, *args, **kwargs):
        return gifts_utils.gifts_destroy(self, request, *args, **kwargs)

# ********************************** ContractChange put delete post get **********************************

class ContractChangeListCreateAPIView(generics.ListCreateAPIView):
    queryset = ContractChange.objects.all()
    serializer_class = ContractChangeSerializer
    permission_classes = [contract_permissions.ContractChangePermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            old_contract = serializer.validated_data.get("old_contract")
            if old_contract == None:
                return Response({"detail": "Dəyişmək istədiyiniz müqaviləni daxil edin."}, status=status.HTTP_400_BAD_REQUEST)
            payment_style = serializer.validated_data.get("payment_style")
            if payment_style == None:
                payment_style = "KREDİT"
            loan_term = serializer.validated_data.get("loan_term")
            if loan_term == None:
                return Response({"detail": "Dəyişim statusunda installment müddəti əlavə olunmalıdır."}, status=status.HTTP_400_BAD_REQUEST)

            product = serializer.validated_data.get("product")
            if product == None:
                return Response({"detail": "Dəyişim statusunda product əlavə olunmalıdır."}, status=status.HTTP_400_BAD_REQUEST)

            old_contract.modified_product_status = "DƏYİŞİLMİŞ MƏHSUL"
            old_contract.contract_status = "DÜŞƏN"
            old_contract.save()

            if payment_style == "KREDİT":
                initial_payment = old_contract.initial_payment
                if initial_payment == None:
                    initial_payment = 0
                initial_payment_debt = old_contract.initial_payment_debt
                if initial_payment_debt == None:
                    initial_payment_debt = 0

                odenilmis_amount = 0

                odenilmis_payment_dateleri = Installment.objects.filter(contract = old_contract, payment_status="ÖDƏNƏN")

                if len(odenilmis_payment_dateleri) != 0:
                    for odenmis_date in odenilmis_payment_dateleri:
                        odenilmis_amount = float(odenilmis_amount) + float(odenmis_date.price) + float(initial_payment) + float(initial_payment_debt)
                else:
                    odenilmis_amount = float(odenilmis_amount) + float(initial_payment) + float(initial_payment_debt)

                total_amount = float(product.price) * int(old_contract.product_quantity)

                office = old_contract.office
                try:
                    warehouse = get_object_or_404(Warehouse, office=office)
                except:
                    return Response({"detail": "Warehouse tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    cashbox = get_object_or_404(OfficeCashbox, office=office)
                except:
                    return Response({"detail": "Office Kassa tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    stok = get_object_or_404(Stock, warehouse=warehouse, product=product)
                except:
                    return Response({"detail": "Stockda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)
                if (stok.quantity < int(old_contract.product_quantity)):
                    return Response({"detail": "Stockda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

                cashbox_balance = cashbox.balance
                remaining_debt = 0

                if (int(loan_term) == 31):
                    # Kredit muddeti 31 ay daxil edilerse
                    return Response({"detail": "Maksimum installment müddəti 30 aydır"}, status=status.HTTP_400_BAD_REQUEST)
                
                if (int(loan_term) == 0):
                    # Kredit muddeti 0 ay daxil edilerse
                    return Response({"detail": "Kredit müddəti 0 ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)

                remaining_debt = float(total_amount) - float(odenilmis_amount)
                contract_utils.reduce_product_from_stock(stok, int(old_contract.product_quantity))

                yeni_contract = Contract.objects.create(
                    group_leader = old_contract.group_leader,
                    manager1 = old_contract.manager1,
                    manager2 = old_contract.manager2,
                    customer = old_contract.customer,
                    product = product,
                    product_quantity = old_contract.product_quantity,
                    total_amount = total_amount,
                    electronic_signature = old_contract.electronic_signature,
                    contract_date = datetime.date.today(),
                    company = old_contract.company,
                    office = old_contract.office,
                    remaining_debt = remaining_debt,
                    payment_style = payment_style,
                    modified_product_status = "DƏYİŞİLMİŞ MƏHSUL",
                    loan_term = loan_term,
                    initial_payment = odenilmis_amount,
                    initial_payment_debt = 0,
                    initial_payment_date = datetime.date.today(),
                    initial_payment_debt_date = None,
                    initial_payment_status = "BİTMİŞ",
                    initial_payment_debt_status = "YOXDUR",
                    cancelled_date = None,
                    compensation_income = None,
                    compensation_expense = None,
                )
                yeni_contract.save()

            serializer.save()
            return Response({"detail": "Müqavilə imzalandı"}, status=status.HTTP_201_CREATED)
        else:
            traceback.print_exc()
            return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

# ********************************** demo sale put delete post get **********************************

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
            count = instance.count + float(count_q)
            serializer.save(count=count)
            return Response({"detail": "Demo əlavə olundu"})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Əməliyyat yerinə yetirildi"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_test_installment(request):
    """
    Contract imzalanmadan aylara dusen amounti gormek ucun funksiya

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
    product = Product.objects.get(id=product_id)
    contract_date_str = instance.data.get("contract_date")
    contract_date = datetime.datetime.strptime(contract_date_str, '%d-%m-%Y')

    initial_payment = instance.data.get("initial_payment")
    initial_payment_debt = instance.data.get("initial_payment_debt")

    umumi_installment = []
    
    def loan_term_func(loan_term, product_quantity):
        loan_term_yeni = loan_term * product_quantity
        return loan_term_yeni

    if(payment_style == "KREDİT"):
        # now = datetime.datetime.today().strftime('%d-%m-%Y')
        now = contract_date
        inc_month = pd.date_range(now, periods = loan_term+1, freq='M')
        initial_payment = initial_payment
        initial_payment_debt = initial_payment_debt

        if(initial_payment is not None):
            initial_payment = float(initial_payment)
        
        if(initial_payment_debt is not None):
            initial_payment_debt = float(initial_payment_debt)

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
