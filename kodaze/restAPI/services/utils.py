from rest_framework import status
import datetime
from rest_framework.response import Response
from cashbox.models import OfisKassa
from salary.models import KreditorPrim, MaasGoruntuleme

from product.models import (
    Mehsullar,
)

from contract.models import (
    Muqavile, 
    MuqavileKreditor,
)

from services.models import (
    ServisOdeme, 
    Servis
)
from warehouse.models import (
    Anbar, 
    Stok,
)

import traceback
import pandas as pd

from rest_framework.generics import get_object_or_404

from restAPI.contract.utils.muqavile_utils import k_medaxil
from restAPI.cashbox.utils import (
    holding_umumi_balans_hesabla, 
    pul_axini_create,
    ofis_balans_hesabla, 
)
def create_is_auto_services_when_update_service(muqavile, created, kartric_novu, **kwargs):
    """
        Muqavile imzalanarken create olan servislerin vaxti catdiqda ve
        yerine yetirildikde avtomatik yeni servisin qurulmasina xidmet eden method
    """
    if created:
        instance=muqavile
        indi = instance.muqavile_tarixi

        month = None
        if kartric_novu == "KARTRIC6AY":
            month = '6M'
        elif kartric_novu == "KARTRIC12AY":
            month = '12M'
        elif kartric_novu == "KARTRIC18AY":
            month = '18M'
        elif kartric_novu == "KARTRIC24AY":
            month = '24M'

        print(f"{kartric_novu=}")
        d = pd.to_datetime(f"{indi.year}-{indi.month}-{indi.day}")
        month_service = pd.date_range(start=d, periods=2, freq=month)[1]
        anbar = get_object_or_404(Anbar, ofis=instance.ofis)
        
        kartric = Mehsullar.objects.filter(kartric_novu=kartric_novu, shirket=instance.shirket)
        print(f"{kartric=}")
        for c in kartric:
            stok = Stok.objects.filter(anbar=anbar, mehsul=c)[0]
            if stok == None or stok.say == 0:
                return Response({"detail":f"Anbarın stokunda {c.mehsulun_adi} məhsulu yoxdur"}, status=status.HTTP_404_NOT_FOUND)
        
        q = 0
        while(q<instance.mehsul_sayi):
            for i in range(1):
                servis_qiymeti = 0
                for j in kartric:
                    servis_qiymeti += float(j.qiymet)
                    
                    stok = Stok.objects.filter(anbar=anbar, mehsul=j)[0]
                    stok.say = stok.say - 1
                    stok.save()
                    if (stok.say == 0):
                        stok.delete()

                if(indi.day < 29):
                    servis = Servis.objects.create(
                        muqavile=instance,
                        servis_tarix = f"{month_service.year}-{month_service.month}-{indi.day}",
                        servis_qiymeti=servis_qiymeti,
                        is_auto=True
                    )
                elif(indi.day == 31 or indi.day == 30 or indi.day == 29):
                    if(month_service.day <= indi.day):
                        servis = Servis.objects.create(
                            muqavile=instance,
                            servis_tarix = f"{month_service.year}-{month_service.month}-{month_service.day}",
                            servis_qiymeti=servis_qiymeti,
                            is_auto=True
                        )
                    elif(month_service.day > indi.day):
                        servis = Servis.objects.create(
                            muqavile=instance,
                            servis_tarix = f"{month_service.year}-{month_service.month}-{indi.day}",
                            servis_qiymeti=servis_qiymeti,
                            is_auto=True
                        )
                servis.mehsullar.set(kartric)
                servis.save()
            q+=1

def servis_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)

    if serializer.is_valid():
        muqavile_id = request.data.get("muqavile_id")
        muqavile = Muqavile.objects.get(id=muqavile_id)

        kredit = request.data.get("kredit")

        kredit_muddeti = request.data.get("kredit_muddeti")

        if bool(kredit) == True: 
            if ((int(kredit_muddeti) == 0) or (int(kredit_muddeti) == 1)):
                return Response({"detail":"Kredit statusu qeyd olunarsa kredit müddəti 0 və ya 1 daxil edilə bilməz"}, status=status.HTTP_400_BAD_REQUEST)
        endirim = serializer.validated_data.get("endirim")
        if endirim == None:
            endirim = 0
        servis_tarixi = request.data.get("servis_tarixi")
        yerine_yetirildi = request.data.get("yerine_yetirildi")
        ilkin_odenis = request.data.get("ilkin_odenis")
        if ilkin_odenis == None:
            ilkin_odenis = 0
        
        mehsullar = []
        mehsullar_data = request.data.get("mehsullar_id")
        for meh in mehsullar_data:
            mhs = Mehsullar.objects.get(pk=int(meh))
            mehsullar.append(mhs)
        anbar = get_object_or_404(Anbar, ofis=muqavile.ofis)
        for j in mehsullar:
            try:
                stok = get_object_or_404(Stok, anbar=anbar, mehsul=j)
            except Exception:
                return Response({"detail": f"Anbarın stokunda {j.mehsulun_adi} məhsulu yoxdur"}, status=status.HTTP_404_NOT_FOUND)

        servis_qiymeti = 0
        for i in mehsullar:
            servis_qiymeti += i.qiymet
            try:
                stok = get_object_or_404(Stok, anbar=anbar, mehsul=i)
                stok.say = stok.say - 1
                stok.save()
                if (stok.say == 0):
                    stok.delete()
            except Exception:
                traceback.print_exc()
                return Response({"detail":"Anbarın stokunda məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

        if float(endirim) >  float(servis_qiymeti):
            return Response({"detail":"Endirim qiyməti servis qiymətindən çox ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)

        odenilecek_umumi_mebleg = float(servis_qiymeti) - float(ilkin_odenis) - float(endirim)
        
        serializer.save(odenilecek_umumi_mebleg=odenilecek_umumi_mebleg, servis_qiymeti=servis_qiymeti)
        return Response({"detail":"Servis düzəldildi"}, status=status.HTTP_200_OK)
    else:
        return Response({"detail":"Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

def servis_update(self, request, *args, **kwargs):
    servis = self.get_object()
    serializer = self.get_serializer(servis, data=request.data, partial=True)

    if serializer.is_valid():
        muqavile = servis.muqavile
        ofis=muqavile.ofis
        servis_tarix = serializer.validated_data.get("servis_tarix")
        mehsullar = serializer.validated_data.get("mehsullar")
        
        kredit = serializer.validated_data.get("kredit")
        kredit_muddeti = serializer.validated_data.get("kredit_muddeti")
        ilkin_odenis = serializer.validated_data.get("ilkin_odenis")

        endirim = serializer.validated_data.get("endirim")

        u_yerine_yetirildi = serializer.validated_data.get("yerine_yetirildi")
        
        yerine_yetirildi = servis.yerine_yetirildi

        anbar = get_object_or_404(Anbar, ofis=muqavile.ofis)

        ofis_kassa = get_object_or_404(OfisKassa, ofis=muqavile.ofis) 
        
        user = self.request.user

        for j in servis.mehsullar.all():
            try:
                stok = get_object_or_404(Stok, anbar=anbar, mehsul=j)
            except Exception:
                return Response({"detail": f"Anbarın stokunda {j.mehsulun_adi} məhsulu yoxdur"}, status=status.HTTP_404_NOT_FOUND)

        if bool(u_yerine_yetirildi) == True:
            for i in servis.mehsullar.all():
                try:
                    stok = get_object_or_404(Stok, anbar=anbar, mehsul=i)
                    stok.say = stok.say - 1
                    stok.save()
                    if (stok.say == 0):
                        stok.delete()
                except Exception:
                    return Response({"detail":"Anbarın stokunda məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

            servis_odemeleri = ServisOdeme.objects.filter(servis=servis)
            for s in servis_odemeleri:
                s.odendi = True
                s.save()

                if servis.is_auto == True:
                    print("Yeni servis create edilmə prosesi işə düşdü")
                    kartric_novu = servis.mehsullar.all()[0].kartric_novu
                    create_is_auto_services_when_update_service(muqavile=muqavile, created=True, kartric_novu=kartric_novu)

                ilkin_balans = holding_umumi_balans_hesabla()
                print(f"{ilkin_balans=}")
                ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

                qeyd = f"Kreditor - {user.asa}, müştəri - {muqavile.musteri.asa}, servis ödənişi"
                k_medaxil(ofis_kassa, s.odenilecek_mebleg, user, qeyd)
                sonraki_balans = holding_umumi_balans_hesabla()
                print(f"{sonraki_balans=}")
                ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
                pul_axini_create(
                    ofis=muqavile.ofis,
                    shirket=ofis.shirket,
                    aciqlama=qeyd,
                    ilkin_balans=ilkin_balans,
                    sonraki_balans=sonraki_balans,
                    ofis_ilkin_balans=ofis_ilkin_balans,
                    ofis_sonraki_balans=ofis_sonraki_balans,
                    emeliyyat_eden=user,
                    emeliyyat_uslubu="MƏDAXİL",
                    miqdar=float(s.odenilecek_mebleg)
                )
        serializer.save()
        return Response({"detail":"Proses yerinə yetirildi"}, status=status.HTTP_200_OK)


def servis_odeme_update(self, request, *args, **kwargs):
    servis_odeme = self.get_object()
    serializer = self.get_serializer(servis_odeme, data=request.data, partial=True)
    
    if serializer.is_valid():
        odendi = serializer.validated_data.get("odendi")
        muqavile = servis_odeme.servis.muqavile
        try:
            muqavile_kreditor = MuqavileKreditor.objects.filter(muqavile=muqavile)[0]
        except:
            return Response({"detail":"Kreditor təyin edilməyib"}, status=status.HTTP_400_BAD_REQUEST)
        kreditor = muqavile_kreditor.kreditor

        kreditor_prim_all = KreditorPrim.objects.all()

        kreditor_prim = kreditor_prim_all[0]

        prim_faizi = kreditor_prim.prim_faizi

        indi = datetime.date.today()

        bu_ay = f"{indi.year}-{indi.month}-{1}"

        maas_goruntulenme_kreditor = MaasGoruntuleme.objects.get(isci=kreditor, tarix=bu_ay)

        user = self.request.user

        ofis_kassa = get_object_or_404(OfisKassa, ofis=muqavile.ofis) 

        if odendi is not None:
            if bool(odendi) == True:
                servisler_qs = ServisOdeme.objects.filter(servis=servis_odeme.servis, odendi=False)
                servisler = list(servisler_qs)
                if servis_odeme == servisler[-1]:
                    servis_odeme.servis.yerine_yetirildi = True
                    servis_odeme.servis.save()
                    servis_odeme.odendi = True
                    servis_odeme.save()
                    if servis_odeme.servis.is_auto == True:
                        print("Yeni servis create edilmə prosesi işə düşdü")
                        kartric_novu = servis_odeme.servis.mehsullar.all()[0].kartric_novu
                        print(f"{kartric_novu=}")
                        create_is_auto_services_when_update_service(muqavile=muqavile, created=True, kartric_novu=kartric_novu)

                    ilkin_balans = holding_umumi_balans_hesabla()
                    print(f"{ilkin_balans=}")
                    ofis_ilkin_balans = ofis_balans_hesabla(ofis=muqavile.ofis)
                    
                    qeyd = f"Kreditor - {user.asa}, müştəri - {muqavile.musteri.asa}, servis ödənişi"
                    k_medaxil(ofis_kassa, servis_odeme.odenilecek_mebleg, user, qeyd)
                    kreditorun_servisden_alacagi_mebleg = (float(servis_odeme.odenilecek_mebleg) * int(prim_faizi)) / 100

                    sonraki_balans = holding_umumi_balans_hesabla()
                    print(f"{sonraki_balans=}")
                    ofis_sonraki_balans = ofis_balans_hesabla(ofis=muqavile.ofis)
                    pul_axini_create(
                        ofis=muqavile.ofis,
                        shirket=muqavile.ofis.shirket,
                        aciqlama=qeyd,
                        ilkin_balans=ilkin_balans,
                        sonraki_balans=sonraki_balans,
                        ofis_ilkin_balans=ofis_ilkin_balans,
                        ofis_sonraki_balans=ofis_sonraki_balans,
                        emeliyyat_eden=user,
                        emeliyyat_uslubu="MƏDAXİL",
                        miqdar=float(servis_odeme.odenilecek_mebleg)
                    )

                    maas_goruntulenme_kreditor.yekun_maas = maas_goruntulenme_kreditor.yekun_maas + kreditorun_servisden_alacagi_mebleg
                    maas_goruntulenme_kreditor.save()
                serializer.save()
                return Response({"detail":"Servis məbləği ödəndi"}, status=status.HTTP_200_OK)
        serializer.save()
        return Response({"detail":"Servis Ödəmə müvəffəqiyyətlə yeniləndi"}, status=status.HTTP_200_OK)