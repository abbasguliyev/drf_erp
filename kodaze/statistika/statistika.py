from account.models import User
from account.api.serializers import UserSerializer
from contract.api.serializers import DemoSalesSerializer, ContractSerializer
from services.api.serializers import ServiceStatistikaSerializer
from contract.api.filters import DemoSalesFilter, ContractFilter
from services.api.filters import ServiceFilter
from contract.models import DemoSales, Contract
from services.models import Service
from salary.models import (
    SalaryView
)
from salary.api.serializers import (
    SalaryViewSerializer
)
from rest_framework import generics, status

from rest_framework.response import Response

from salary.api import permissions as salary_permissions

from django_filters.rest_framework import DjangoFilterBackend

from salary.api.filters import (
    SalaryViewFilter
)

from contract.api import permissions as contract_permissions
from services.api import permissions as service_permission

from account.api import permissions as account_permissions
from account.api.selectors import user_list
from account.api.filters import (
    UserFilter,
)

from salary.api.selectors import salary_view_list

class SalaryViewStatistikaAPIView(generics.ListAPIView):
    queryset = salary_view_list()
    serializer_class = SalaryViewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalaryViewFilter
    permission_classes = [salary_permissions.SalaryViewPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.queryset
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = self.queryset.filter(employee__company=request.user.company, employee__office=request.user.office)
            queryset = self.queryset.filter(employee__company=request.user.company)
        else:
            queryset = self.queryset
        queryset = self.filter_queryset(queryset)
    
        sale_quantity = 0
        for q in queryset:
            sale_quantity += q.sale_quantity

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([{'umumi_sale_quantity':sale_quantity, 'data':serializer.data}])

        serializer = self.get_serializer(queryset, many=True)
        return Response([{'umumi_sale_quantity':sale_quantity, 'data':serializer.data}])

class DemoStatistikaListAPIView(generics.ListAPIView):
    queryset = DemoSales.objects.all()
    serializer_class = DemoSalesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DemoSalesFilter
    permission_classes = [contract_permissions.DemoSalesPermissions]

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        demo_quantityi = 0
        sale_count = 0
        for q in queryset:
            demo_quantityi += q.count

        for q in queryset:
            sale_count += q.sale_count

        try:
            demo_sale_nisbeti = float(demo_quantityi)/float(sale_count)
        except:
           return Response({'detail': "Satış quantityı 0-a bərabərdir"}, status=status.HTTP_400_BAD_REQUEST) 

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([{'umumi_demo_quantityi':demo_quantityi, 'umumi_sale_quantity':sale_count, 'demo_sale_nisbeti':demo_sale_nisbeti, 'data':serializer.data}])

        serializer = self.get_serializer(queryset, many=True)
        return Response([{'umumi_demo_quantityi':demo_quantityi, 'umumi_sale_quantity':sale_count, 'demo_sale_nisbeti':demo_sale_nisbeti, 'data':serializer.data}])

class ContractStatistikaAPIView(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilter
    permission_classes = [contract_permissions.ContractPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Contract.objects.all()
            dusen = Contract.objects.filter(contract_status="DÜŞƏN")
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = Contract.objects.filter(company=request.user.company, office=request.user.office)
                dusen = Contract.objects.filter(contract_status="DÜŞƏN", company=request.user.company, office=request.user.office)
            queryset = Contract.objects.filter(company=request.user.company)
            dusen = Contract.objects.filter(contract_status="DÜŞƏN", company=request.user.company)
        else:
            queryset = Contract.objects.all()
            dusen = Contract.objects.filter(contract_status="DÜŞƏN")
        queryset = self.filter_queryset(queryset)
        queryset_dusen = self.filter_queryset(dusen)

        contract_quantityi = queryset.count()
        dusen_contract_quantityi = queryset_dusen.count()
        try:
            dusme_faizi = (float(dusen_contract_quantityi) * 100)/float(contract_quantityi)
        except:
           return Response({'detail': "Müqavilə quantityı 0-a bərabərdir"}, status=status.HTTP_400_BAD_REQUEST) 

        umumi_remaining_debt = 0
        for i in queryset:
            umumi_remaining_debt += i.remaining_debt

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'contract_quantityi':contract_quantityi, 'dusen_contract_quantityi': dusen_contract_quantityi, 'dusme_faizi': dusme_faizi, 'umumi_remaining_debt': umumi_remaining_debt, 'data':serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return Response([
            {'contract_quantityi':contract_quantityi, 'dusen_contract_quantityi':dusen_contract_quantityi, 'dusme_faizi': dusme_faizi, 'umumi_remaining_debt': umumi_remaining_debt, 'data':serializer.data}
        ])

class UserStatistikaList(generics.ListAPIView):
    queryset = user_list()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    permission_classes = [account_permissions.UserPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = user_list()
            deactive_user = user_list().filter(is_active=False)
            active_user = user_list().filter(is_active=True)
        elif request.user.company is not None:
            if request.user.office is not None:
                queryset = user_list().filter(company=request.user.company, office= request.user.office)
                deactive_user = user_list().filter(is_active=False, company= request.user.company, office= request.user.office)
                active_user = user_list().filter(is_active=True, company= request.user.company, office= request.user.office)
            queryset = user_list().filter(company=request.user.company)
            deactive_user = user_list().filter(is_active=False, company= request.user.company)
            active_user = user_list().filter(is_active=True, company= request.user.company)

        else:
            queryset = user_list()
            deactive_user = user_list().filter(is_active=False)
            active_user = user_list().filter(is_active=True)
        
        d_queryset = self.filter_queryset(deactive_user)
        a_queryset = self.filter_queryset(active_user)
        queryset = self.filter_queryset(queryset)

        deactive_user_count = d_queryset.count()
        active_user_count = a_queryset.count()
        user_count = queryset.count()
        try:
            azad_olma_nisbeti = float(active_user_count)/float(deactive_user_count)
        except:
           return Response({'detail': "İşdən çıxan işçi quantityı 0-a bərabərdir"}, status=status.HTTP_400_BAD_REQUEST) 

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'deactive_user_count': deactive_user_count, 'active_user_count': active_user_count, 'azad_olma_nisbeti': azad_olma_nisbeti, 'user_count': user_count, 'data':serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return Response([
                {'deactive_user_count': deactive_user_count, 'active_user_count': active_user_count, 'azad_olma_nisbeti': azad_olma_nisbeti, 'user_count': user_count, 'data':serializer.data}
            ])

class ServiceStatistikaAPIView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceStatistikaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter
    permission_classes = [service_permission.ServicePermissions]

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

        service_quantityi = queryset.count()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'service_quantityi': service_quantityi, 'data':serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return Response([
                {'service_quantityi': service_quantityi, 'data':serializer.data}
            ])