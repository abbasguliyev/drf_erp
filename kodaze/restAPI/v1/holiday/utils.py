import datetime
import traceback
import pandas as pd
from rest_framework import status
from rest_framework.response import Response
from salary.models import Kesinti, MaasGoruntuleme
from account.models import User
from restAPI.v1.holiday.serializers import (
    HoldingIstisnaIsciSerializer,
    IsciGunlerSerializer,
    HoldingGunlerSerializer,
    KomandaGunlerSerializer,
    KomandaIstisnaIsciSerializer, 
    OfisGunlerSerializer,
    OfisIstisnaIsciSerializer,
    ShirketGunlerSerializer,
    ShirketIstisnaIsciSerializer,
    ShobeGunlerSerializer,
    ShobeIstisnaIsciSerializer,
    VezifeGunlerSerializer,
    VezifeIstisnaIsciSerializer
)
from holiday.models import (
    IsciGunler,
    KomandaGunler,
    OfisGunler,
    ShirketGunler,
    ShobeGunler,
    VezifeGunler
)
# --------------------------------------------------------------------------------------------------------------------------

def company_isci_tetil_hesablama(company, company_name, tarix, tetil_gunleri, is_gunleri_count, qeyri_is_gunu_count, istisna_isciler=list()):
    """
    Bu method holding, shirket, ofis, shobe, komanda ve vezife-nin is ve qeyri is gunleri hesablanan zaman onlarla elaqeli olan
    iscilerin is ve qeyri is gunlerini hesablamaq ucundur. Hemcinin eger holding-in is ve qeyri is gunleri hesablanirsa bu zaman yuxarida
    sadaladigim diger obyektlerinde is ve qeyri is gunleri uygun olaraq deyisir.
    """
    if(company=="holding"):
        isciler = list(User.objects.all())
        ofis_gunler = OfisGunler.objects.filter(tarix=tarix)
        for o in ofis_gunler:
            o.is_gunleri_count = is_gunleri_count
            o.qeyri_is_gunu_count = qeyri_is_gunu_count
            o.tetil_gunleri = tetil_gunleri
            o.save()
        shirket_gunler = ShirketGunler.objects.filter(tarix=tarix)
        for s in shirket_gunler:
            s.is_gunleri_count = is_gunleri_count
            s.qeyri_is_gunu_count = qeyri_is_gunu_count
            s.tetil_gunleri = tetil_gunleri
            s.save()
        shobe_gunler = ShobeGunler.objects.filter(tarix=tarix)
        for sh in shobe_gunler:
            sh.is_gunleri_count = is_gunleri_count
            sh.qeyri_is_gunu_count = qeyri_is_gunu_count
            sh.tetil_gunleri = tetil_gunleri
            sh.save()
        vezife_gunler = VezifeGunler.objects.filter(tarix=tarix)
        for v in vezife_gunler:
            v.is_gunleri_count = is_gunleri_count
            v.qeyri_is_gunu_count = qeyri_is_gunu_count
            v.tetil_gunleri = tetil_gunleri
            v.save()
        komanda_gunler = KomandaGunler.objects.filter(tarix=tarix)
        for k in komanda_gunler:
            k.is_gunleri_count = is_gunleri_count
            k.qeyri_is_gunu_count = qeyri_is_gunu_count
            k.tetil_gunleri = tetil_gunleri
            k.save()
    elif(company=="shirket"):
        isciler = list(User.objects.filter(shirket=company_name))
    elif(company=="shobe"):
        isciler = list(User.objects.filter(shobe=company_name))
    elif(company=="ofis"):
        isciler = list(User.objects.filter(ofis=company_name))
    elif(company=="komanda"):
        isciler = list(User.objects.filter(komanda=company_name))
    elif(company=="vezife"):
        isciler = list(User.objects.filter(vezife=company_name))

    z = 1
    for isci in isciler:
        if istisna_isciler != list():
            if isci in istisna_isciler:
                continue
        try:
            isci_gunler = IsciGunler.objects.get(isci=isci, tarix=tarix)
            isci_gunler.tetil_gunleri = tetil_gunleri
            isci_gunler.is_gunleri_count = is_gunleri_count
            isci_gunler.qeyri_is_gunu_count = qeyri_is_gunu_count
            isci_gunler.save()
        except:
            traceback.print_exc()
        z+=1
    return True

def instisna_isci_create(serializer, company, company_name, obj_gunler):
    tarix = obj_gunler.tarix
    obj_gunler_tetil_gunleri = obj_gunler.tetil_gunleri
    date_list = []
    k_date_list = []
    
    tetil_gunleri = serializer.validated_data.get("tetil_gunleri")
    tetil_gunleri_l = tetil_gunleri.rstrip("]").lstrip("[").split(",")
    for i in tetil_gunleri_l:
        new_el = i.strip().strip("'").strip('"')
        date_list.append(new_el)

    istisna_isciler = serializer.validated_data.get("istisna_isciler")

    # indi = datetime.date.today()

    # d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    # next_m = d + pd.offsets.MonthBegin(1)

    days_in_mont = pd.Period(f"{tarix.year}-{tarix.month}-{1}").days_in_month

    for isci in istisna_isciler:
        isci_gunler = IsciGunler.objects.get(isci=isci, tarix=tarix)
        if isci_gunler.tetil_gunleri is not None:
            isci_gunler_tetil_gunleri = obj_gunler_tetil_gunleri.rstrip("]").lstrip("[").split(",")
            for i in isci_gunler_tetil_gunleri:
                new_el = i.strip().strip("'").strip('"')
                k_date_list.append(new_el)

            for i in date_list:
                if i in k_date_list:
                    k_date_list.remove(i)
        isci_gunler.tetil_gunleri = k_date_list
        isci_gunler.is_gunleri_count = float(days_in_mont) - len(k_date_list)
        isci_gunler.qeyri_is_gunu_count = len(k_date_list)
        isci_gunler.save()

    serializer.save(tetil_gunleri=date_list, istisna_isciler=istisna_isciler)

def istisna_isci_update(serializer, company, company_name, obj_gunler, obj_istisna_isci):
    tarix = obj_gunler.tarix
    obj_gunler_tetil_gunleri = obj_gunler.tetil_gunleri

    date_list = []
    k_date_list = []
    q_date_list = []

    k_tetil_gunleri = obj_istisna_isci.tetil_gunleri
    k_tetil_gunleri_l = k_tetil_gunleri.rstrip("]").lstrip("[").split(",")
    for i in k_tetil_gunleri_l:
        new_el = i.strip().strip("'").strip('"')
        k_date_list.append(new_el)

    # indi = datetime.date.today()

    # d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    # next_m = d + pd.offsets.MonthBegin(1)

    days_in_mont = pd.Period(f"{tarix.year}-{tarix.month}-{1}").days_in_month

    tetil_gunleri = serializer.validated_data.get("tetil_gunleri")
    if tetil_gunleri == None:
        tetil_gunleri = k_date_list
        tetil_gunleri_l = tetil_gunleri
        date_list = k_date_list
    else:
        tetil_gunleri_l = tetil_gunleri.rstrip("]").lstrip("[").split(",")
        for i in tetil_gunleri_l:
            new_el = i.strip().strip("'").strip('"')
            date_list.append(new_el)

    u_istisna_isciler = []

    istisna_isciler = serializer.validated_data.get("istisna_isciler")
    if istisna_isciler == None:
        istisna_isciler = list(obj_istisna_isci.istisna_isciler.all())

    k_istisna_isciler = list(obj_istisna_isci.istisna_isciler.all())

    for i in k_istisna_isciler:
        u_istisna_isciler.append(i)

    for j in istisna_isciler:
        if j in u_istisna_isciler:
            continue
        else:
            u_istisna_isciler.append(j)

    if (
        (serializer.validated_data.get("istisna_isciler") == None or serializer.validated_data.get("istisna_isciler") == "") 
        and 
        (serializer.validated_data.get("tetil_gunleri") != None)
    ):
        for isci in u_istisna_isciler:
            isci_gunler = IsciGunler.objects.get(isci=isci, tarix=tarix)
            if isci_gunler.tetil_gunleri is not None:
                isci_gunler_tetil_gunleri = obj_gunler_tetil_gunleri.rstrip("]").lstrip("[").split(",")
                for i in isci_gunler_tetil_gunleri:
                    new_el = i.strip().strip("'").strip('"')
                    q_date_list.append(new_el)

                if len(date_list) == len(q_date_list):
                    isci_gunler.tetil_gunleri = list(q_date_list)
                    isci_gunler.is_gunleri_count = float(days_in_mont)
                    isci_gunler.qeyri_is_gunu_count = 0
                    isci_gunler.save()
                else:
                    for i in date_list:
                        if i in q_date_list:
                            q_date_list.remove(i)
                        isci_gunler.tetil_gunleri = list(q_date_list)
                        isci_gunler.is_gunleri_count = float(days_in_mont) - len(date_list)
                        isci_gunler.qeyri_is_gunu_count = len(date_list)
                        isci_gunler.save()
    elif(
        (serializer.validated_data.get("istisna_isciler") != None) 
        and 
        (serializer.validated_data.get("tetil_gunleri") == None)
    ):
        for isci in istisna_isciler:
            isci_gunler = IsciGunler.objects.get(isci=isci, tarix=tarix)
            if isci_gunler.tetil_gunleri is not None:
                isci_gunler_tetil_gunleri = obj_gunler_tetil_gunleri.rstrip("]").lstrip("[").split(",")
                for i in isci_gunler_tetil_gunleri:
                    new_el = i.strip().strip("'").strip('"')
                    q_date_list.append(new_el)

                for i in date_list:
                    if i in q_date_list:
                        q_date_list.remove(i)
            isci_gunler.tetil_gunleri = list(q_date_list)
            isci_gunler.is_gunleri_count = float(days_in_mont) - len(date_list)
            isci_gunler.qeyri_is_gunu_count = len(date_list)
            isci_gunler.save()
    elif(
        (serializer.validated_data.get("istisna_isciler") != None) 
        and 
        (serializer.validated_data.get("tetil_gunleri") != None)
    ):
        for isci in u_istisna_isciler:
            isci_gunler = IsciGunler.objects.get(isci=isci, tarix=tarix)
            if isci_gunler.tetil_gunleri is not None:
                isci_gunler_tetil_gunleri = obj_gunler_tetil_gunleri.rstrip("]").lstrip("[").split(",")
                for i in isci_gunler_tetil_gunleri:
                    new_el = i.strip().strip("'").strip('"')
                    q_date_list.append(new_el)

                if len(date_list) == len(q_date_list):
                    isci_gunler.tetil_gunleri = list(q_date_list)
                    isci_gunler.is_gunleri_count = float(days_in_mont)
                    isci_gunler.qeyri_is_gunu_count = 0
                    isci_gunler.save()
                else:
                    for i in date_list:
                        if i in q_date_list:
                            q_date_list.remove(i)
                        isci_gunler.tetil_gunleri = list(q_date_list)
                        isci_gunler.is_gunleri_count = float(days_in_mont) - len(date_list)
                        isci_gunler.qeyri_is_gunu_count = len(date_list)
                        isci_gunler.save()

    # serializer.save(tetil_gunleri=date_list, istisna_isciler=u_istisna_isciler)
    serializer.save()

def istisna_isci_delete(obj_gunler, obj_istisna_isci):
    istisna_isciler = obj_istisna_isci.istisna_isciler.all()

    tarix = obj_gunler.tarix

    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_mont = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    for isci in istisna_isciler:
        isci_gunler = IsciGunler.objects.get(isci=isci, tarix=tarix)
        if isci_gunler.tetil_gunleri is not None: 
            isci_gunler.tetil_gunleri = None
            isci_gunler.is_gunleri_count = float(days_in_mont)
            isci_gunler.qeyri_is_gunu_count = 0
            isci_gunler.save()


def isci_tetil_gunleri_calc(serializer, obj):
    date_list = []
    odenisli_icaze_date_list = []
    odenissiz_icaze_date_list = []

    isci = obj.isci

    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_mont = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    tetil_gunleri = serializer.validated_data.get("tetil_gunleri")
    if tetil_gunleri is not None:
        tetil_gunleri_l = tetil_gunleri.rstrip("]").lstrip("[").split(",")
    else:
        tetil_gunleri_l = []
        
    for i in tetil_gunleri_l:
        new_el = i.strip().strip("'").strip('"')
        date_list.append(new_el)

    icaze_gunleri_odenisli = serializer.validated_data.get("icaze_gunleri_odenisli")
    icaze_gunleri_odenissiz = serializer.validated_data.get("icaze_gunleri_odenissiz")

    if icaze_gunleri_odenisli is not None:
        icaze_gunleri_odenisli_l = icaze_gunleri_odenisli.rstrip("]").lstrip("[").split(",")
    else:
        icaze_gunleri_odenisli_l = []

    if icaze_gunleri_odenissiz is not None:
        icaze_gunleri_odenissiz_l = icaze_gunleri_odenissiz.rstrip("]").lstrip("[").split(",")
    else:
        icaze_gunleri_odenissiz_l = []

    for i in icaze_gunleri_odenisli_l:
        new_elm = i.strip().strip("'").strip('"')
        odenisli_icaze_date_list.append(new_elm)

    for i in icaze_gunleri_odenissiz_l:
        new_elm1 = i.strip().strip("'").strip('"')
        odenissiz_icaze_date_list.append(new_elm1)

    k_qeyri_is_gunleri = obj.qeyri_is_gunu_count

    qeyri_is_gunu_count = float(len(date_list)) + float(len(odenisli_icaze_date_list)) + float(len(odenissiz_icaze_date_list))
    is_gunleri_count = float(days_in_mont)
    is_gunleri_count = float(is_gunleri_count) - float(qeyri_is_gunu_count)

    is_odenisli = serializer.validated_data.get("is_odenisli")
    odenis_meblegi = serializer.validated_data.get("odenis_meblegi")

    if is_odenisli == True:
        try:
            maas_goruntulenme = MaasGoruntuleme.objects.get(isci=isci, tarix=d)
            maas_goruntulenme.yekun_maas = float(maas_goruntulenme.yekun_maas) - float(odenis_meblegi)
            maas_goruntulenme.save()
            kesinti = Kesinti.objects.create(isci=isci, mebleg=odenis_meblegi, qeyd="ödənişli icazə ilə əlaqədar", kesinti_tarixi=indi)
            kesinti.save()
        except:
            return Response({"detail": "Maaş kartında xəta"}, status=status.HTTP_400_BAD_REQUEST)

    # serializer.save(tetil_gunleri=date_list, is_gunleri_count=is_gunleri_count, qeyri_is_gunu_count=qeyri_is_gunu_count)
    serializer.save( is_gunleri_count=is_gunleri_count, qeyri_is_gunu_count=qeyri_is_gunu_count)
    return True

def isci_tetil_gunleri_delete(obj_gunler):
    
    indi = datetime.date.today()

    d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")

    next_m = d + pd.offsets.MonthBegin(1)

    days_in_mont = pd.Period(f"{next_m.year}-{next_m.month}-{1}").days_in_month

    obj_gunler.tetil_gunleri = None
    obj_gunler.icaze_gunleri_odenisli = None
    obj_gunler.icaze_gunleri_odenissiz = None
    obj_gunler.is_gunleri_count = float(days_in_mont)
    obj_gunler.qeyri_is_gunu_count = 0
    obj_gunler.save()
    

def gunler_update(serializer, company, company_name, obj_gunler):
    tarix = obj_gunler.tarix
    is_gunleri_count = obj_gunler.is_gunleri_count
    qeyri_is_gunu_count = obj_gunler.qeyri_is_gunu_count
    date_list = []
    k_date_list = []
    u_date_list = []

    k_tetil_gunleri = obj_gunler.tetil_gunleri
    if k_tetil_gunleri is not None:
        k_tetil_gunleri_l = k_tetil_gunleri.rstrip("]").lstrip("[").split(",")
        for i in k_tetil_gunleri_l:
            new_el = i.strip().strip("'").strip('"')
            k_date_list.append(new_el)
    else:
        k_date_list = []

    tetil_gunleri = serializer.validated_data.get("tetil_gunleri")
    if tetil_gunleri == None:
        tetil_gunleri = k_date_list
        tetil_gunleri_l = tetil_gunleri
    else:
        tetil_gunleri_l = tetil_gunleri.rstrip("]").lstrip("[").split(",")
        for i in tetil_gunleri_l:
            new_el = i.strip().strip("'").strip('"')
            date_list.append(new_el)

    # for i in date_list:
    #     u_date_list.append(i)

    # for j in k_date_list:
    #     if j in u_date_list:
    #         continue
    #     else:
    #         u_date_list.append(j)
    k_qeyri_is_gunleri = obj_gunler.qeyri_is_gunu_count
    qeyri_is_gunu_count = len(date_list)
    k_is_gunleri_count = obj_gunler.is_gunleri_count
    is_gunleri_count = float(k_is_gunleri_count) - (float(qeyri_is_gunu_count) - float(k_qeyri_is_gunleri))
    company_isci_tetil_hesablama(
        company=company, 
        company_name=company_name, 
        tarix=tarix, 
        tetil_gunleri=date_list, 
        is_gunleri_count=is_gunleri_count, 
        qeyri_is_gunu_count=qeyri_is_gunu_count
    )

    serializer.save(
        qeyri_is_gunu_count = qeyri_is_gunu_count, 
        is_gunleri_count = is_gunleri_count,
        tetil_gunleri=date_list
    )

# --------------------------------------------------------------------------------------------------------------------------

def holding_gunler_update(self, request, *args, **kwargs):
    holding_gunler = self.get_object()
    serializer = HoldingGunlerSerializer(holding_gunler, data=request.data, partial=True)
    try:
        if serializer.is_valid():
            gunler_update(serializer=serializer, company="holding", company_name=holding_gunler.holding, obj_gunler=holding_gunler)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        traceback.print_exc()
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)


def holding_istisna_isci_gunler_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        holding_gunler = serializer.validated_data.get("gunler")
        instisna_isci_create(serializer=serializer, company="holding", company_name=holding_gunler.holding, obj_gunler=holding_gunler)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def holding_istisna_isci_gunler_update(self, request, *args, **kwargs):
    holding_istisna_isci_obj = self.get_object()
    serializer = HoldingIstisnaIsciSerializer(holding_istisna_isci_obj, data=request.data, partial=True)
    
    if serializer.is_valid():
        
        istisna_isci_update(serializer=serializer, company="holding", company_name=holding_istisna_isci_obj.gunler.holding, obj_gunler=holding_istisna_isci_obj.gunler, obj_istisna_isci=holding_istisna_isci_obj)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def holding_istisna_isci_gunler_delete(self, request, *args, **kwargs):
    holding_istisna_isci_obj = self.get_object()
    try:
        istisna_isci_delete(
            obj_gunler=holding_istisna_isci_obj.gunler, 
            obj_istisna_isci=holding_istisna_isci_obj
        )
        holding_istisna_isci_obj.delete()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------------

def ofis_gunler_update(self, request, *args, **kwargs):
    ofis_gunler = self.get_object()
    serializer = OfisGunlerSerializer(ofis_gunler, data=request.data, partial=True)

    if serializer.is_valid():
        gunler_update(serializer=serializer, company="ofis", company_name=ofis_gunler.ofis, obj_gunler=ofis_gunler)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def ofis_istisna_isci_gunler_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        ofis_gunler = serializer.validated_data.get("gunler")
        instisna_isci_create(serializer=serializer, company="ofis", company_name=ofis_gunler.ofis, obj_gunler=ofis_gunler)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def ofis_istisna_isci_gunler_update(self, request, *args, **kwargs):
    ofis_istisna_isci_obj = self.get_object()
    serializer = OfisIstisnaIsciSerializer(ofis_istisna_isci_obj, data=request.data, partial=True)
    
    if serializer.is_valid():
        istisna_isci_update(serializer=serializer, company="ofis", company_name=ofis_istisna_isci_obj.gunler.ofis, obj_gunler=ofis_istisna_isci_obj.gunler, obj_istisna_isci=ofis_istisna_isci_obj)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def ofis_istisna_isci_gunler_delete(self, request, *args, **kwargs):
    ofis_istisna_isci_obj = self.get_object()
    try:
        istisna_isci_delete(
            obj_gunler=ofis_istisna_isci_obj.gunler, 
            obj_istisna_isci=ofis_istisna_isci_obj
        )
        ofis_istisna_isci_obj.delete()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------------

def shirket_gunler_update(self, request, *args, **kwargs):
    shirket_gunler = self.get_object()
    serializer = ShirketGunlerSerializer(shirket_gunler, data=request.data, partial=True)

    if serializer.is_valid():
        gunler_update(serializer=serializer, company="shirket", company_name=shirket_gunler.shirket, obj_gunler=shirket_gunler)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def shirket_istisna_isci_gunler_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        shirket_gunler = serializer.validated_data.get("gunler")
        instisna_isci_create(serializer=serializer, company="shirket", company_name=shirket_gunler.shirket, obj_gunler=shirket_gunler)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def shirket_istisna_isci_gunler_update(self, request, *args, **kwargs):
    shirket_istisna_isci_obj = self.get_object()
    serializer = ShirketIstisnaIsciSerializer(shirket_istisna_isci_obj, data=request.data, partial=True)
    
    if serializer.is_valid():
        istisna_isci_update(serializer=serializer, company="shirket", company_name=shirket_istisna_isci_obj.gunler.shirket, obj_gunler=shirket_istisna_isci_obj.gunler, obj_istisna_isci=shirket_istisna_isci_obj)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def shirket_istisna_isci_gunler_delete(self, request, *args, **kwargs):
    shirket_istisna_isci_obj = self.get_object()
    try:
        istisna_isci_delete(
            obj_gunler=shirket_istisna_isci_obj.gunler, 
            obj_istisna_isci=shirket_istisna_isci_obj
        )
        shirket_istisna_isci_obj.delete()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------------

def shobe_gunler_update(self, request, *args, **kwargs):
    shobe_gunler = self.get_object()
    serializer = ShobeGunlerSerializer(shobe_gunler, data=request.data, partial=True)

    if serializer.is_valid():
        gunler_update(serializer=serializer, company="shobe", company_name=shobe_gunler.shobe, obj_gunler=shobe_gunler)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def shobe_istisna_isci_gunler_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        shobe_gunler = serializer.validated_data.get("gunler")
        instisna_isci_create(serializer=serializer, company="shobe", company_name=shobe_gunler.shobe, obj_gunler=shobe_gunler)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def shobe_istisna_isci_gunler_update(self, request, *args, **kwargs):
    shobe_istisna_isci_obj = self.get_object()
    serializer = ShobeIstisnaIsciSerializer(shobe_istisna_isci_obj, data=request.data, partial=True)
    
    if serializer.is_valid():
        istisna_isci_update(serializer=serializer, company="shobe", company_name=shobe_istisna_isci_obj.gunler.shobe, obj_gunler=shobe_istisna_isci_obj.gunler, obj_istisna_isci=shobe_istisna_isci_obj)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def shobe_istisna_isci_gunler_delete(self, request, *args, **kwargs):
    shobe_istisna_isci_obj = self.get_object()
    try:
        istisna_isci_delete(
            obj_gunler=shobe_istisna_isci_obj.gunler, 
            obj_istisna_isci=shobe_istisna_isci_obj
        )
        shobe_istisna_isci_obj.delete()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)
# ------------------------------------------------------------------------------------------------

def komanda_gunler_update(self, request, *args, **kwargs):
    komanda_gunler = self.get_object()
    serializer = KomandaGunlerSerializer(komanda_gunler, data=request.data, partial=True)
    if serializer.is_valid():
        gunler_update(serializer=serializer, company="komanda", company_name=komanda_gunler.komanda, obj_gunler=komanda_gunler)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def komanda_istisna_isci_gunler_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        komanda_gunler = serializer.validated_data.get("komanda_gunler")
        instisna_isci_create(serializer=serializer, company="komanda", company_name=komanda_gunler.komanda, obj_gunler=komanda_gunler)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def komanda_istisna_isci_gunler_update(self, request, *args, **kwargs):
    komanda_istisna_isci_obj = self.get_object()
    serializer = KomandaIstisnaIsciSerializer(komanda_istisna_isci_obj, data=request.data, partial=True)
    
    if serializer.is_valid():
        istisna_isci_update(serializer=serializer, company="komanda", company_name=komanda_istisna_isci_obj.gunler.komanda, obj_gunler=komanda_istisna_isci_obj.gunler, obj_istisna_isci=komanda_istisna_isci_obj)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def komanda_istisna_isci_gunler_delete(self, request, *args, **kwargs):
    komanda_istisna_isci_obj = self.get_object()
    try:
        istisna_isci_delete(
            obj_gunler=komanda_istisna_isci_obj.gunler, 
            obj_istisna_isci=komanda_istisna_isci_obj
        )
        komanda_istisna_isci_obj.delete()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------------

def vezife_gunler_update(self, request, *args, **kwargs):
    vezife_gunler = self.get_object()
    serializer = VezifeGunlerSerializer(vezife_gunler, data=request.data, partial=True)
    if serializer.is_valid():
        gunler_update(serializer=serializer, company="vezife", company_name=vezife_gunler.vezife, obj_gunler=vezife_gunler)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def vezife_istisna_isci_gunler_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        vezife_gunler = serializer.validated_data.get("gunler")
        instisna_isci_create(serializer=serializer, company="vezife", company_name=vezife_gunler.vezife, obj_gunler=vezife_gunler)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def vezife_istisna_isci_gunler_update(self, request, *args, **kwargs):
    vezife_istisna_isci_obj = self.get_object()
    serializer = VezifeIstisnaIsciSerializer(vezife_istisna_isci_obj, data=request.data, partial=True)
    
    if serializer.is_valid():
        istisna_isci_update(serializer=serializer, company="vezife", company_name=vezife_istisna_isci_obj.gunler.vezife, obj_gunler=vezife_istisna_isci_obj.gunler, obj_istisna_isci=vezife_istisna_isci_obj)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)
    
def vezife_istisna_isci_gunler_delete(self, request, *args, **kwargs):
    vezife_istisna_isci_obj = self.get_object()
    try:
        istisna_isci_delete(
            obj_gunler=vezife_istisna_isci_obj.gunler, 
            obj_istisna_isci=vezife_istisna_isci_obj
        )
        vezife_istisna_isci_obj.delete()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)
# ------------------------------------------------------------------------------------------------

def user_gunler_update(self, request, *args, **kwargs):
    user_gunler = self.get_object()
    serializer = IsciGunlerSerializer(user_gunler, data=request.data, partial=True)
    if serializer.is_valid():
        isci_tetil_gunleri_calc(serializer, user_gunler)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def user_gunler_patch(self, request, *args, **kwargs):
    user_gunler = self.get_object()
    serializer = IsciGunlerSerializer(user_gunler, data=request.data, partial=True)
    if serializer.is_valid():
        isci_tetil_gunleri_calc(serializer, user_gunler)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

def user_gunler_delete(self, request, *args, **kwargs):
    user_gunler = self.get_object()
    try:
        isci_tetil_gunleri_delete(
            obj_gunler=user_gunler
        )
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    except:
        return Response({"detail": "Xəta!"}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------------


