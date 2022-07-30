from account.models import User
from restAPI.account.serializers import UserSerializer
from restAPI.contract.serializers import DemoSatisSerializer, MuqavileSerializer
from restAPI.services.serializers import ServisStatistikaSerializer
from restAPI.contract.filters import DemoSatisFilter, MuqavileFilter
from restAPI.services.filters import ServisFilter
from contract.models import DemoSatis, Muqavile
from services.models import Servis
from salary.models import (
    MaasGoruntuleme
)
from restAPI.salary.serializers import (
    MaasGoruntulemeSerializer
)
from rest_framework import generics, status

from rest_framework.response import Response

from restAPI.salary import permissions as maas_permissions

from django_filters.rest_framework import DjangoFilterBackend

from restAPI.salary.filters import (
    MaasGoruntulemeFilter
)

from restAPI.contract import permissions as muqavile_permissions
from restAPI.services import permissions as servis_permission

from restAPI.account import permissions as account_permissions

from restAPI.account.filters import (
    UserFilter,
)

class MaasGoruntulemeStatistikaAPIView(generics.ListAPIView):
    queryset = MaasGoruntuleme.objects.all()
    serializer_class = MaasGoruntulemeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MaasGoruntulemeFilter
    permission_classes = [maas_permissions.MaasGoruntulemePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = MaasGoruntuleme.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = MaasGoruntuleme.objects.filter(isci__shirket=request.user.shirket, isci__ofis=request.user.ofis)
            queryset = MaasGoruntuleme.objects.filter(isci__shirket=request.user.shirket)
        else:
            queryset = MaasGoruntuleme.objects.all()
        queryset = self.filter_queryset(queryset)
    
        satis_sayi = 0
        for q in queryset:
            satis_sayi += q.satis_sayi

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([{'umumi_satis_sayi':satis_sayi, 'data':serializer.data}])

        serializer = self.get_serializer(queryset, many=True)
        return Response([{'umumi_satis_sayi':satis_sayi, 'data':serializer.data}])

class DemoStatistikaListAPIView(generics.ListAPIView):
    queryset = DemoSatis.objects.all()
    serializer_class = DemoSatisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DemoSatisFilter
    permission_classes = [muqavile_permissions.DemoSatisPermissions]

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        demo_sayi = 0
        sale_count = 0
        for q in queryset:
            demo_sayi += q.count

        for q in queryset:
            sale_count += q.sale_count

        try:
            demo_satis_nisbeti = float(demo_sayi)/float(sale_count)
        except:
           return Response({'detail': "Satış sayı 0-a bərabərdir"}, status=status.HTTP_400_BAD_REQUEST) 

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([{'umumi_demo_sayi':demo_sayi, 'umumi_satis_sayi':sale_count, 'demo_satis_nisbeti':demo_satis_nisbeti, 'data':serializer.data}])

        serializer = self.get_serializer(queryset, many=True)
        return Response([{'umumi_demo_sayi':demo_sayi, 'umumi_satis_sayi':sale_count, 'demo_satis_nisbeti':demo_satis_nisbeti, 'data':serializer.data}])

class MuqavileStatistikaAPIView(generics.ListAPIView):
    queryset = Muqavile.objects.all()
    serializer_class = MuqavileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MuqavileFilter
    permission_classes = [muqavile_permissions.MuqavilePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Muqavile.objects.all()
            dusen = Muqavile.objects.filter(muqavile_status="DÜŞƏN")
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = Muqavile.objects.filter(shirket=request.user.shirket, ofis=request.user.ofis)
                dusen = Muqavile.objects.filter(muqavile_status="DÜŞƏN", shirket=request.user.shirket, ofis=request.user.ofis)
            queryset = Muqavile.objects.filter(shirket=request.user.shirket)
            dusen = Muqavile.objects.filter(muqavile_status="DÜŞƏN", shirket=request.user.shirket)
        else:
            queryset = Muqavile.objects.all()
            dusen = Muqavile.objects.filter(muqavile_status="DÜŞƏN")
        queryset = self.filter_queryset(queryset)
        queryset_dusen = self.filter_queryset(dusen)

        muqavile_sayi = queryset.count()
        dusen_muqavile_sayi = queryset_dusen.count()
        try:
            dusme_faizi = (float(dusen_muqavile_sayi) * 100)/float(muqavile_sayi)
        except:
           return Response({'detail': "Müqavilə sayı 0-a bərabərdir"}, status=status.HTTP_400_BAD_REQUEST) 

        umumi_qaliq_borc = 0
        for i in queryset:
            umumi_qaliq_borc += i.qaliq_borc

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'muqavile_sayi':muqavile_sayi, 'dusen_muqavile_sayi': dusen_muqavile_sayi, 'dusme_faizi': dusme_faizi, 'umumi_qaliq_borc': umumi_qaliq_borc, 'data':serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return Response([
            {'muqavile_sayi':muqavile_sayi, 'dusen_muqavile_sayi':dusen_muqavile_sayi, 'dusme_faizi': dusme_faizi, 'umumi_qaliq_borc': umumi_qaliq_borc, 'data':serializer.data}
        ])

class UserStatistikaList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    permission_classes = [account_permissions.UserPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = User.objects.all()
            deactive_user = User.objects.filter(is_active=False)
            active_user = User.objects.filter(is_active=True)
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = User.objects.filter(shirket=request.user.shirket, ofis=request.user.ofis)
                deactive_user = User.objects.filter(is_active=False, shirket=request.user.shirket, ofis=request.user.ofis)
                active_user = User.objects.filter(is_active=True, shirket=request.user.shirket, ofis=request.user.ofis)
            queryset = User.objects.filter(shirket=request.user.shirket)
            deactive_user = User.objects.filter(is_active=False, shirket=request.user.shirket)
            active_user = User.objects.filter(is_active=True, shirket=request.user.shirket)

        else:
            queryset = User.objects.all()
            deactive_user = User.objects.filter(is_active=False)
            active_user = User.objects.filter(is_active=True)
        
        d_queryset = self.filter_queryset(deactive_user)
        a_queryset = self.filter_queryset(active_user)
        queryset = self.filter_queryset(queryset)

        deactive_user_count = d_queryset.count()
        active_user_count = a_queryset.count()
        user_count = queryset.count()
        try:
            azad_olma_nisbeti = float(active_user_count)/float(deactive_user_count)
        except:
           return Response({'detail': "İşdən çıxan işçi sayı 0-a bərabərdir"}, status=status.HTTP_400_BAD_REQUEST) 

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

class ServisStatistikaAPIView(generics.ListAPIView):
    queryset = Servis.objects.all()
    serializer_class = ServisStatistikaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServisFilter
    permission_classes = [servis_permission.ServisPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Servis.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = Servis.objects.filter(muqavile__shirket=request.user.shirket, muqavile__ofis=request.user.ofis)
            queryset = Servis.objects.filter(muqavile__shirket=request.user.shirket)
        else:
            queryset = Servis.objects.all()
        
        queryset = self.filter_queryset(queryset)

        servis_sayi = queryset.count()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'servis_sayi': servis_sayi, 'data':serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return Response([
                {'servis_sayi': servis_sayi, 'data':serializer.data}
            ])