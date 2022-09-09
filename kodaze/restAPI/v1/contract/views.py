import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status, generics

import pandas as pd

from rest_framework.response import Response
from rest_framework import generics
from cashbox.models import OfisKassa

from rest_framework.decorators import api_view
from product.models import Mehsullar
from warehouse.models import Stok, Anbar

from restAPI.v1.contract.serializers import (
    DemoSatisSerializer,
    DeyisimSerializer,
    MuqavileSerializer,
    MuqavileHediyyeSerializer,
    OdemeTarixSerializer,
    MuqavileKreditorSerializer
)

from contract.models import (
    MuqavileKreditor,
    MuqavileHediyye, 
    Muqavile, 
    OdemeTarix,  
    Deyisim, 
    DemoSatis
)


from restAPI.v1.contract.utils import (
    odeme_tarixleri_utils,
    muqavile_utils,
    muqavile_hediyye_utils,
)

from django_filters.rest_framework import DjangoFilterBackend

from restAPI.v1.contract.filters import (
    DemoSatisFilter,
    MuqavileHediyyeFilter,
    OdemeTarixFilter,
    MuqavileFilter,
)

from restAPI.v1.contract import permissions as contract_permissions

# ********************************** muqavile get post put delete **********************************

class MuqavileListCreateAPIView(generics.ListCreateAPIView):
    queryset = Muqavile.objects.select_related(
                    'group_leader', 
                    'menecer1', 
                    'menecer2', 
                    'musteri', 
                    'mehsul', 
                    'shirket', 
                    'ofis', 
                    'shobe'
                ).all()
    serializer_class = MuqavileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MuqavileFilter
    permission_classes = [contract_permissions.MuqavilePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Muqavile.objects.select_related(
                    'group_leader', 
                    'menecer1', 
                    'menecer2', 
                    'musteri', 
                    'mehsul', 
                    'shirket', 
                    'ofis', 
                    'shobe'
                ).all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = Muqavile.objects.select_related(
                    'group_leader', 
                    'menecer1', 
                    'menecer2', 
                    'musteri', 
                    'mehsul', 
                    'shirket', 
                    'ofis', 
                    'shobe'
                ).filter(shirket=request.user.shirket, ofis=request.user.ofis)
            queryset = Muqavile.objects.select_related(
                    'group_leader', 
                    'menecer1', 
                    'menecer2', 
                    'musteri', 
                    'mehsul', 
                    'shirket', 
                    'ofis', 
                    'shobe'
                ).filter(shirket=request.user.shirket)
        else:
            queryset = Muqavile.objects.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return muqavile_utils.muqavile_create(self, request, *args, **kwargs)


class MuqavileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Muqavile.objects.all()
    serializer_class = MuqavileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MuqavileFilter
    permission_classes = [contract_permissions.MuqavilePermissions]

    def patch(self, request, *args, **kwargs):
        return muqavile_utils.muqavile_patch(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return muqavile_utils.muqavile_update(self, request, *args, **kwargs)


# ********************************** odeme tarixi put get post delete **********************************


class OdemeTarixListCreateAPIView(generics.ListCreateAPIView):
    queryset = OdemeTarix.objects.all()
    serializer_class = OdemeTarixSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OdemeTarixFilter
    permission_classes = [contract_permissions.OdemeTarixleriPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = OdemeTarix.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = OdemeTarix.objects.filter(muqavile__shirket=request.user.shirket, muqavile__ofis=request.user.ofis)
            queryset = OdemeTarix.objects.filter(muqavile__shirket=request.user.shirket)
        else:
            queryset = OdemeTarix.objects.all()
        
        queryset = self.filter_queryset(queryset)

        umumi_miqdar = 0

        for q in queryset:
            umumi_miqdar += q.qiymet

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response([
                {'umumi_miqdar': umumi_miqdar, 'data':serializer.data}
            ])

        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response([
                {'umumi_miqdar': umumi_miqdar, 'data':serializer.data}
            ])

    def create(self, request, *args, **kwargs):
        return muqavile_utils.muqavile_create(self, request, *args, **kwargs)

class OdemeTarixDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = OdemeTarix.objects.all()
    serializer_class = OdemeTarixSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['muqavile']
    filterset_class = OdemeTarixFilter
    permission_classes = [contract_permissions.OdemeTarixleriPermissions]

    # # PATCH SORGUSU
    # def patch(self, request, *args, **kwargs):
    #     return odeme_tarixleri_utils.odeme_tarixi_patch(self, request, *args, **kwargs)

    # PUT SORGUSU
    def update(self, request, *args, **kwargs):
        return odeme_tarixleri_utils.odeme_tarixi_update(self, request, *args, **kwargs)


# ********************************** hediyye put delete post get **********************************
class MuqavileHediyyeListCreateAPIView(generics.ListCreateAPIView):
    queryset = MuqavileHediyye.objects.all()
    serializer_class = MuqavileHediyyeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MuqavileHediyyeFilter
    permission_classes = [contract_permissions.MuqavileHediyyePermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = MuqavileHediyye.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = MuqavileHediyye.objects.filter(muqavile__shirket=request.user.shirket, muqavile__ofis=request.user.ofis)
            queryset = MuqavileHediyye.objects.filter(muqavile__shirket=request.user.shirket)
        else:
            queryset = MuqavileHediyye.objects.all()
        
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return muqavile_hediyye_utils.muqavile_hediyye_create(self, request, *args, **kwargs)


class MuqavileHediyyeDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = MuqavileHediyye.objects.all()
    serializer_class = MuqavileHediyyeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MuqavileHediyyeFilter
    permission_classes = [contract_permissions.MuqavileHediyyePermissions]

    def destroy(self, request, *args, **kwargs):
        return muqavile_hediyye_utils.muqavile_hediyye_destroy(self, request, *args, **kwargs)

# ********************************** Deyisim put delete post get **********************************

class DeyisimListCreateAPIView(generics.ListCreateAPIView):
    queryset = Deyisim.objects.all()
    serializer_class = DeyisimSerializer
    permission_classes = [contract_permissions.DeyisimPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            kohne_muqavile = serializer.validated_data.get("kohne_muqavile")
            if kohne_muqavile == None:
                return Response({"detail": "Dəyişmək istədiyiniz müqaviləni daxil edin."}, status=status.HTTP_400_BAD_REQUEST)
            odenis_uslubu = serializer.validated_data.get("odenis_uslubu")
            if odenis_uslubu == None:
                odenis_uslubu = "KREDİT"
            kredit_muddeti = serializer.validated_data.get("kredit_muddeti")
            if kredit_muddeti == None:
                return Response({"detail": "Dəyişim statusunda kredit müddəti əlavə olunmalıdır."}, status=status.HTTP_400_BAD_REQUEST)

            mehsul = serializer.validated_data.get("mehsul")
            if mehsul == None:
                return Response({"detail": "Dəyişim statusunda mehsul əlavə olunmalıdır."}, status=status.HTTP_400_BAD_REQUEST)

            kohne_muqavile.deyisilmis_mehsul_status = "DƏYİŞİLMİŞ MƏHSUL"
            kohne_muqavile.muqavile_status = "DÜŞƏN"
            kohne_muqavile.save()

            if odenis_uslubu == "KREDİT":
                ilkin_odenis = kohne_muqavile.ilkin_odenis
                if ilkin_odenis == None:
                    ilkin_odenis = 0
                ilkin_odenis_qaliq = kohne_muqavile.ilkin_odenis_qaliq
                if ilkin_odenis_qaliq == None:
                    ilkin_odenis_qaliq = 0

                odenilmis_mebleg = 0

                odenilmis_odeme_tarixleri = OdemeTarix.objects.filter(muqavile = kohne_muqavile, odenme_status="ÖDƏNƏN")

                if len(odenilmis_odeme_tarixleri) != 0:
                    for odenmis_tarix in odenilmis_odeme_tarixleri:
                        odenilmis_mebleg = float(odenilmis_mebleg) + float(odenmis_tarix.qiymet) + float(ilkin_odenis) + float(ilkin_odenis_qaliq)
                else:
                    odenilmis_mebleg = float(odenilmis_mebleg) + float(ilkin_odenis) + float(ilkin_odenis_qaliq)

                muqavile_umumi_mebleg = float(mehsul.qiymet) * int(kohne_muqavile.mehsul_sayi)

                ofis = kohne_muqavile.ofis
                try:
                    anbar = get_object_or_404(Anbar, ofis=ofis)
                except:
                    return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    ofis_kassa = get_object_or_404(OfisKassa, ofis=ofis)
                except:
                    return Response({"detail": "Ofis Kassa tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    stok = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)
                except:
                    return Response({"detail": "Stokda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)
                if (stok.say < int(kohne_muqavile.mehsul_sayi)):
                    return Response({"detail": "Stokda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

                ofis_kassa_balans = ofis_kassa.balans
                qaliq_borc = 0

                if (int(kredit_muddeti) == 31):
                    # Kredit muddeti 31 ay daxil edilerse
                    return Response({"detail": "Maksimum kredit müddəti 30 aydır"}, status=status.HTTP_400_BAD_REQUEST)
                
                if (int(kredit_muddeti) == 0):
                    # Kredit muddeti 31 ay daxil edilerse
                    return Response({"detail": "Kredit müddəti 0 ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)

                qaliq_borc = float(muqavile_umumi_mebleg) - float(odenilmis_mebleg)
                muqavile_utils.stok_mehsul_ciximi(stok, int(kohne_muqavile.mehsul_sayi))

                yeni_muqavile = Muqavile.objects.create(
                    group_leader = kohne_muqavile.group_leader,
                    menecer1 = kohne_muqavile.menecer1,
                    menecer2 = kohne_muqavile.menecer2,
                    musteri = kohne_muqavile.musteri,
                    mehsul = mehsul,
                    mehsul_sayi = kohne_muqavile.mehsul_sayi,
                    muqavile_umumi_mebleg = muqavile_umumi_mebleg,
                    elektron_imza = kohne_muqavile.elektron_imza,
                    muqavile_tarixi = datetime.date.today(),
                    shirket = kohne_muqavile.shirket,
                    ofis = kohne_muqavile.ofis,
                    shobe = kohne_muqavile.shobe,
                    qaliq_borc = qaliq_borc,
                    odenis_uslubu = odenis_uslubu,
                    deyisilmis_mehsul_status = "DƏYİŞİLMİŞ MƏHSUL",
                    kredit_muddeti = kredit_muddeti,
                    ilkin_odenis = odenilmis_mebleg,
                    ilkin_odenis_qaliq = 0,
                    ilkin_odenis_tarixi = datetime.date.today(),
                    ilkin_odenis_qaliq_tarixi = None,
                    ilkin_odenis_status = "BİTMİŞ",
                    qaliq_ilkin_odenis_status = "YOXDUR",
                    dusme_tarixi = None,
                    kompensasiya_medaxil = None,
                    kompensasiya_mexaric = None,
                )
                yeni_muqavile.save()

            serializer.save()
            return Response({"detail": "Müqavilə imzalandı"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

# ********************************** demo satis put delete post get **********************************

class DemoSatisListAPIView(generics.ListAPIView):
    queryset = DemoSatis.objects.all()
    serializer_class = DemoSatisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DemoSatisFilter
    permission_classes = [contract_permissions.DemoSatisPermissions]


class DemoSatisDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DemoSatis.objects.all()
    serializer_class = DemoSatisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DemoSatisFilter
    permission_classes = [contract_permissions.DemoSatisPermissions]

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
def create_test_kredit(request):
    """
    Muqavile imzalanmadan aylara dusen meblegi gormek ucun funksiya

    request = {
        "kredit_muddeti":10,
        "mehsul_sayi":10,
        "odenis_uslubu":"KREDİT",
        "muqavile_tarixi":"2022-07-28",
        "ilkin_odenis":100,
        "ilkin_odenis_qaliq":0,
        "mehsul_id":1,
        "kredit_muddeti":10
    }
    """
    instance = request
    kredit_muddeti = instance.data.get("kredit_muddeti")
    mehsul_sayi = instance.data.get("mehsul_sayi")
    mehsul_id = instance.data.get("mehsul_id")
    odenis_uslubu = instance.data.get("odenis_uslubu")
    mehsul = Mehsullar.objects.get(id=mehsul_id)
    muqavile_tarixi_str = instance.data.get("muqavile_tarixi")
    muqavile_tarixi = datetime.datetime.strptime(muqavile_tarixi_str, '%d-%m-%Y')

    ilkin_odenis = instance.data.get("ilkin_odenis")
    ilkin_odenis_qaliq = instance.data.get("ilkin_odenis_qaliq")

    umumi_kredit = []
    
    def kredit_muddeti_func(kredit_muddeti, mehsul_sayi):
        kredit_muddeti_yeni = kredit_muddeti * mehsul_sayi
        return kredit_muddeti_yeni

    if(odenis_uslubu == "KREDİT"):
        # indi = datetime.datetime.today().strftime('%d-%m-%Y')
        indi = muqavile_tarixi
        inc_month = pd.date_range(indi, periods = kredit_muddeti+1, freq='M')
        ilkin_odenis = ilkin_odenis
        ilkin_odenis_qaliq = ilkin_odenis_qaliq

        if(ilkin_odenis is not None):
            ilkin_odenis = float(ilkin_odenis)
        
        if(ilkin_odenis_qaliq is not None):
            ilkin_odenis_qaliq = float(ilkin_odenis_qaliq)

        mehsulun_qiymeti = mehsul_sayi * mehsul.qiymet
        if(ilkin_odenis_qaliq == 0):
            ilkin_odenis_tam = ilkin_odenis
        elif(ilkin_odenis_qaliq != 0):
            ilkin_odenis_tam = ilkin_odenis + ilkin_odenis_qaliq
        aylara_gore_odenecek_umumi_mebleg = mehsulun_qiymeti - ilkin_odenis_tam
        
        if(kredit_muddeti > 0):
            aylara_gore_odenecek_mebleg = aylara_gore_odenecek_umumi_mebleg // kredit_muddeti

            qaliq = aylara_gore_odenecek_mebleg * (kredit_muddeti - 1)
            son_aya_odenecek_mebleg = aylara_gore_odenecek_umumi_mebleg - qaliq

            i = 1
            while(i<=kredit_muddeti):
                if(i == kredit_muddeti):
                    if(indi.day < 29):
                        kredit = {}
                        kredit["ay_no"] = i
                        kredit["tarix"] = f"{inc_month[i].year}-{inc_month[i].month}-{indi.day}"
                        kredit["qiymet"] = son_aya_odenecek_mebleg
                        umumi_kredit.append(kredit)
                    elif(indi.day == 31 or indi.day == 30 or indi.day == 29):
                        if(inc_month[i].day <= indi.day):
                            kredit = {}
                            kredit["ay_no"] = i
                            kredit["tarix"] = f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}"
                            kredit["qiymet"] = son_aya_odenecek_mebleg
                            umumi_kredit.append(kredit)
                            
                        elif(inc_month[i].day > indi.day):
                            kredit = {}
                            kredit["ay_no"] = i
                            kredit["tarix"] = f"{inc_month[i].year}-{inc_month[i].month}-{indi.day}"
                            kredit["qiymet"] = son_aya_odenecek_mebleg
                            umumi_kredit.append(kredit)
                else:
                    if(indi.day < 29):
                        kredit = {}
                        kredit["ay_no"] = i
                        kredit["tarix"] = f"{inc_month[i].year}-{inc_month[i].month}-{indi.day}"
                        kredit["qiymet"] = aylara_gore_odenecek_mebleg
                        umumi_kredit.append(kredit)
                        
                    elif(indi.day == 31 or indi.day == 30 or indi.day == 29):
                        if(inc_month[i].day <= indi.day):
                            kredit = {}
                            kredit["ay_no"] = i
                            kredit["tarix"] = f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}"
                            kredit["qiymet"] = aylara_gore_odenecek_mebleg
                            umumi_kredit.append(kredit)
                            
                        if(inc_month[i].day > indi.day):
                            kredit = {}
                            kredit["ay_no"] = i
                            kredit["tarix"] = f"{inc_month[i].year}-{inc_month[i].month}-{indi.day}"
                            kredit["qiymet"] = aylara_gore_odenecek_mebleg
                            umumi_kredit.append(kredit)
                i+=1
    return Response(umumi_kredit)


class MuqavileKreditorListCreateAPIView(generics.ListCreateAPIView):
    queryset = MuqavileKreditor.objects.all()
    serializer_class = MuqavileKreditorSerializer
    permission_classes = [contract_permissions.MuqavileKreditorPermissions]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = MuqavileKreditor.objects.all()
        elif request.user.shirket is not None:
            if request.user.ofis is not None:
                queryset = MuqavileKreditor.objects.filter(muqavile__shirket=request.user.shirket, muqavile__ofis=request.user.ofis)
            queryset = MuqavileKreditor.objects.filter(muqavile__shirket=request.user.shirket)
        else:
            queryset = MuqavileKreditor.objects.all()
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
            muqavile = serializer.validated_data.get("muqavile")
            muqavile_kreditor = MuqavileKreditor.objects.filter(muqavile=muqavile)
            if len(muqavile_kreditor)>0:
                return Response({"detail":"Bir müqaviləyə birdən artıq kreditor təyin edilə bilməz"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"detail":"Müqavilə kreditor əlavə olundu"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)

class MuqavileKreditorDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = MuqavileKreditor.objects.all()
    serializer_class = MuqavileKreditorSerializer
    permission_classes = [contract_permissions.MuqavileKreditorPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"Müqavilə kreditor məlumatları yeniləndi"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail":"Məlumatları doğru daxil etdiyinizdən əmin olun"}, status=status.HTTP_400_BAD_REQUEST)
