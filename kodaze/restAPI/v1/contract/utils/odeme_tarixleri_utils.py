import traceback
from cashbox.models import OfisKassa
from income_expense.models import OfisKassaMedaxil
from contract.models import  OdemeTarix
from rest_framework.exceptions import ValidationError
import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
import pandas as pd

from restAPI.v1.contract.serializers import OdemeTarixSerializer

from restAPI.v1.utils.ocean_muqavile_pdf_create import (
    okean_create_muqavile_pdf, 
    okean_muqavile_pdf_canvas, 
    ocean_kredit_create_muqavile_pdf,
    ocean_kredit_muqavile_pdf_canvas
)

from restAPI.v1.utils.magnus_muqavile_pdf_create import (
    magnus_create_muqavile_pdf,
    magnus_muqavile_pdf_canvas,
    magnus_kredit_create_muqavile_pdf,
    magnus_kredit_muqavile_pdf_canvas
)

from restAPI.v1.cashbox.utils import (
    holding_umumi_balans_hesabla, 
    pul_axini_create, 
    ofis_balans_hesabla
)

def create_and_add_pdf_when_muqavile_updated(sender, instance, created, **kwargs):
    if created:
        print("create_and_add_pdf_when_muqavile_updated  işə düşdü")

        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.ofis.shirket.shirket_adi == okean:
            muqavile_pdf_canvas_list = okean_muqavile_pdf_canvas(
                muqavile=instance, musteri=instance.musteri
            )
            muqavile_pdf = okean_create_muqavile_pdf(muqavile_pdf_canvas_list, instance)
        elif instance.ofis.shirket.shirket_adi == magnus:
            muqavile_pdf_canvas_list = magnus_muqavile_pdf_canvas(
                muqavile=instance, musteri=instance.musteri
            )
            muqavile_pdf = magnus_create_muqavile_pdf(muqavile_pdf_canvas_list, instance)
        instance.pdf = muqavile_pdf
        instance.save()

def create_and_add_pdf_when_muqavile_kredit_updated(sender, instance, created, **kwargs):
    if created:
        print("create_and_add_pdf_when_muqavile_kredit_updated işə düşdü")

        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.ofis.shirket.shirket_adi == okean:
            muqavile_pdf_canvas_list = ocean_kredit_muqavile_pdf_canvas(
                muqavile=instance
            )
            muqavile_pdf = ocean_kredit_create_muqavile_pdf(muqavile_pdf_canvas_list, instance)
        elif instance.ofis.shirket.shirket_adi == magnus:
            muqavile_pdf_canvas_list = magnus_kredit_muqavile_pdf_canvas(
                muqavile=instance
            )
            muqavile_pdf = magnus_kredit_create_muqavile_pdf(muqavile_pdf_canvas_list, instance)
        instance.pdf_elave = muqavile_pdf
        instance.save()

def pdf_create_when_muqavile_updated(sender, instance, created):
    create_and_add_pdf_when_muqavile_updated(sender=sender, instance=instance, created=created) 
    create_and_add_pdf_when_muqavile_kredit_updated(sender=sender, instance=instance, created=created)

def k_medaxil(company_kassa, daxil_edilecek_mebleg, vanleader, qeyd):
    yekun_balans = float(daxil_edilecek_mebleg) + float(company_kassa.balans)
    company_kassa.balans = yekun_balans
    company_kassa.save()
    tarix = datetime.date.today()

    medaxil = OfisKassaMedaxil.objects.create(
        medaxil_eden=vanleader,
        ofis_kassa=company_kassa,
        mebleg=daxil_edilecek_mebleg,
        medaxil_tarixi=tarix,
        qeyd=qeyd
    )
    medaxil.save()
    return medaxil

# PATCH sorgusu
def odeme_tarixi_patch(self, request, *args, **kwargs):
    pass

# UPDATE SORGUSU
def odeme_tarixi_update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    odenme_status = request.data.get("odenme_status")
    sertli_odeme_status = request.data.get("sertli_odeme_status")
    gecikdirme_status = request.data.get("gecikdirme_status")
    natamama_gore_odeme_status = request.data.get("natamam_ay_alt_status")
    sifira_gore_odeme_status = request.data.get("buraxilmis_ay_alt_status")
    artiq_odeme_alt_status = request.data.get('artiq_odeme_alt_status')

    user = request.user

    indiki_ay = self.get_object()
    odemek_istediyi_mebleg = request.data.get("qiymet")

    if odemek_istediyi_mebleg == None:
        odemek_istediyi_mebleg = 0

    today = datetime.date.today()

    muqavile = indiki_ay.muqavile
    vanleader = muqavile.vanleader
    musteri = muqavile.musteri
    odenis_uslubu = muqavile.odenis_uslubu
    ofis = muqavile.ofis

    ofis_kassa = get_object_or_404(OfisKassa, ofis=ofis)

    borcu_bagla_status = request.data.get("borcu_bagla_status")

    qaliq_borc = muqavile.qaliq_borc

    qeyd = request.data.get("qeyd")
    if qeyd == None:
        qeyd = ""

    def umumi_mebleg(mehsul_qiymeti, mehsul_sayi):
        muqavile_umumi_mebleg = mehsul_qiymeti * mehsul_sayi
        return muqavile_umumi_mebleg
    
    # BORCU BAĞLA ILE BAGLI EMELIYYATLAR
    if(borcu_bagla_status == "BORCU BAĞLA"):
        odenmeyen_odemetarixler_qs = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")
        odenmeyen_odemetarixler = list(odenmeyen_odemetarixler_qs)

        ay_ucun_olan_mebleg = 0
        for i in odenmeyen_odemetarixler:
            ay_ucun_olan_mebleg = ay_ucun_olan_mebleg + float(i.qiymet)
            i.qiymet = 0
            i.odenme_status = "ÖDƏNƏN"
            i.qeyd = qeyd
            i.save()

        indiki_ay.qiymet = qaliq_borc
        indiki_ay.odenme_status = "ÖDƏNƏN"
        indiki_ay.save()

        muqavile.muqavile_status = "BİTMİŞ"
        qaliq_borc = 0
        muqavile.qaliq_borc = qaliq_borc
        muqavile.borc_baglandi = True
        muqavile.save()

        ilkin_balans = holding_umumi_balans_hesabla()
        print(f"{ilkin_balans=}")
        ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

        qeyd = f"Vanleader - {vanleader.asa}, müştəri - {musteri.asa}, tarix - {today}, ödəniş üslubu - {odenis_uslubu}. Borcu tam bağlandı"
        k_medaxil(ofis_kassa, float(ay_ucun_olan_mebleg), vanleader, qeyd)

        sonraki_balans = holding_umumi_balans_hesabla()
        print(f"{sonraki_balans=}")
        ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
        pul_axini_create(
            ofis=ofis,
            shirket=ofis.shirket,
            aciqlama=qeyd,
            ilkin_balans=ilkin_balans,
            sonraki_balans=sonraki_balans,
            ofis_ilkin_balans=ofis_ilkin_balans,
            ofis_sonraki_balans=ofis_sonraki_balans,
            emeliyyat_eden=user,
            emeliyyat_uslubu="MƏDAXİL",
            miqdar=float(ay_ucun_olan_mebleg)
        )

        pdf_create_when_muqavile_updated(muqavile, muqavile, True)
        return Response({"detail": "Borc tam bağlandı"}, status=status.HTTP_200_OK)

    # GECIKDIRME ILE BAGLI EMELIYYATLAR
    if(
        (indiki_ay.odenme_status == "ÖDƏNMƏYƏN" and gecikdirme_status == "GECİKDİRMƏ")  
        or 
        (indiki_ay.odenme_status == "ÖDƏNMƏYƏN" and request.data.get("tarix") is not None) 
        or 
        (odenme_status == "ÖDƏNMƏYƏN" and gecikdirme_status == "GECİKDİRMƏ") 
        or 
        (odenme_status == "ÖDƏNMƏYƏN" and request.data.get("tarix") is not None)
    ):
        my_time = datetime.datetime.min.time()

        odeme_tarixi_date = indiki_ay.tarix
        odeme_tarixi = datetime.datetime.combine(odeme_tarixi_date, my_time)
        odeme_tarixi_san = datetime.datetime.timestamp(odeme_tarixi)

        gecikdirmek_istediyi_tarix = request.data.get("tarix")
        gecikdirmek_istediyi_tarix_date = datetime.datetime.strptime(gecikdirmek_istediyi_tarix, "%Y-%m-%d")
        gecikdirmek_istediyi_tarix_san = datetime.datetime.timestamp(gecikdirmek_istediyi_tarix_date)

        odenmeyen_odemetarixler_qs = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")
        odenmeyen_odemetarixler = list(odenmeyen_odemetarixler_qs)

        if(indiki_ay == odenmeyen_odemetarixler[-1]):
            try:
                if(gecikdirmek_istediyi_tarix_san < odeme_tarixi_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz tarix keçmiş tarixdir."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(odeme_tarixi_san < gecikdirmek_istediyi_tarix_san):
                    indiki_ay.tarix = gecikdirmek_istediyi_tarix
                    indiki_ay.gecikdirme_status = "GECİKDİRMƏ"
                    # indiki_ay.qeyd = qeyd
                    indiki_ay.save()
                    pdf_create_when_muqavile_updated(muqavile, muqavile, True)
                    return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            except:
                return Response({"detail": "Yeni tarix hal-hazırki tarix ile növbəti ayın tarixi arasında olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
        elif(indiki_ay != odenmeyen_odemetarixler[-1]):
            novbeti_ay = OdemeTarix.objects.get(pk = indiki_ay.id+1)
            novbeti_ay_tarix_date = novbeti_ay.tarix
            novbeti_ay_tarix = datetime.datetime.combine(novbeti_ay_tarix_date, my_time)
            novbeti_ay_tarix_san = datetime.datetime.timestamp(novbeti_ay_tarix)

            try:
                if(novbeti_ay_tarix_san == gecikdirmek_istediyi_tarix_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz tarix növbəti ayın tarixi ilə eynidir."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(gecikdirmek_istediyi_tarix_san < odeme_tarixi_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz tarix keçmiş tarixdir."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(gecikdirmek_istediyi_tarix_san > novbeti_ay_tarix_san):
                    raise ValidationError(detail={"detail": "Tarixi doğru daxil edin!"}, code=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"detail": "Qeyd etdiyiniz tarix növbəti ayın tarixindən böyükdür."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if(odeme_tarixi_san < gecikdirmek_istediyi_tarix_san < novbeti_ay_tarix_san):
                    indiki_ay.tarix = gecikdirmek_istediyi_tarix
                    indiki_ay.gecikdirme_status = "GECİKDİRMƏ"
                    # indiki_ay.qeyd = qeyd
                    indiki_ay.save()
                    pdf_create_when_muqavile_updated(muqavile, muqavile, True)
                    return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            except:
                return Response({"detail": "Yeni tarix hal-hazırki tarix ile növbəti ayın tarixi arasında olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
    elif(indiki_ay.odenme_status != "ÖDƏNMƏYƏN" and gecikdirme_status == "GECİKDİRMƏ"):
        raise ValidationError(detail={"detail": "Gecikdirmə ancaq ödənməmiş ay üçündür"}, code=status.HTTP_400_BAD_REQUEST)
    
    # Natamam Ay odeme statusu ile bagli emeliyyatlar
    if(
        indiki_ay.odenme_status == "ÖDƏNMƏYƏN" 
        and 
        sertli_odeme_status == "NATAMAM AY" 
        and 
        0 < float(odemek_istediyi_mebleg) < indiki_ay.qiymet 
        and 
        natamama_gore_odeme_status != ""
        and 
        natamama_gore_odeme_status is not None
    ):
        ilkin_odenis = muqavile.ilkin_odenis
        ilkin_odenis_qaliq = muqavile.ilkin_odenis_qaliq
        ilkin_odenis_tam = ilkin_odenis + ilkin_odenis_qaliq
        mehsulun_qiymeti = muqavile.muqavile_umumi_mebleg
        indiki_ay.odenme_status = "ÖDƏNƏN"
        indiki_ay.sertli_odeme_status = "NATAMAM AY"
        # indiki_ay.qeyd = qeyd
        indiki_ay.save()


        odenmeyen_odemetarixler = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)
        odemek_istediyi_mebleg = float(request.data.get("qiymet"))
        
        ilkin_balans = holding_umumi_balans_hesabla()
        print(f"{ilkin_balans=}")
        ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

        qeyd = f"Vanleader - {vanleader.asa}, müştəri - {musteri.asa}, tarix - {today}, ödəniş üslubu - {odenis_uslubu}, şərtli ödəmə - {indiki_ay.sertli_odeme_status}"
        k_medaxil(ofis_kassa, float(odemek_istediyi_mebleg), vanleader, qeyd)
        qaliq_borc = muqavile.qaliq_borc
        qaliq_borc = float(qaliq_borc) - float(odemek_istediyi_mebleg)
        muqavile.qaliq_borc = qaliq_borc
        muqavile.save()

        sonraki_balans = holding_umumi_balans_hesabla()
        print(f"{sonraki_balans=}")
        ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
        pul_axini_create(
            ofis=ofis,
            shirket=ofis.shirket,
            aciqlama=qeyd,
            ilkin_balans=ilkin_balans,
            sonraki_balans=sonraki_balans,
            ofis_ilkin_balans=ofis_ilkin_balans,
            ofis_sonraki_balans=ofis_sonraki_balans,
            emeliyyat_eden=user,
            emeliyyat_uslubu="MƏDAXİL",
            miqdar=float(odemek_istediyi_mebleg)
        )
        
        if(natamama_gore_odeme_status == "NATAMAM DİGƏR AYLAR"):
            odenmeyen_pul = indiki_ay.qiymet - odemek_istediyi_mebleg
            odenmeyen_aylar = len(odenmeyen_odemetarixler)

            buraxilmamis_odenmeyen_odemetarixler = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)
            
            aylara_elave_olunacaq_mebleg = odenmeyen_pul // (odenmeyen_aylar - 1)
            b = aylara_elave_olunacaq_mebleg * (odenmeyen_aylar - 1)
            sonuncu_aya_elave_olunacaq_mebleg = odenmeyen_pul - b
            
            indiki_ay.qiymet = odemek_istediyi_mebleg
            indiki_ay.natamam_ay_alt_status = "NATAMAM DİGƏR AYLAR"
            indiki_ay.odenme_status = "ÖDƏNƏN"
            # indiki_ay.qeyd = qeyd
            indiki_ay.save()

            i = 0
            while(i<=(odenmeyen_aylar-1)):
                if(indiki_ay == buraxilmamis_odenmeyen_odemetarixler[i]):
                    i+=1
                    continue
                if(i == (odenmeyen_aylar-1)):
                    odenmeyen_odemetarixler[i].qiymet = odenmeyen_odemetarixler[i].qiymet + sonuncu_aya_elave_olunacaq_mebleg
                    odenmeyen_odemetarixler[i].save()
                else:
                    odenmeyen_odemetarixler[i].qiymet = odenmeyen_odemetarixler[i].qiymet + aylara_elave_olunacaq_mebleg
                    odenmeyen_odemetarixler[i].save()
                i+=1
            if serializer.is_valid():
                serializer.save(odenme_status = "ÖDƏNƏN")
                pdf_create_when_muqavile_updated(muqavile, muqavile, True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        if(natamama_gore_odeme_status == "NATAMAM NÖVBƏTİ AY"):
            indiki_ay = self.get_object()
            natamam_odemek_istediyi_mebleg = indiki_ay.qiymet - odemek_istediyi_mebleg

            novbeti_ay = get_object_or_404(OdemeTarix, pk=self.get_object().id+1)
            novbeti_ay.qiymet = novbeti_ay.qiymet + natamam_odemek_istediyi_mebleg
            novbeti_ay.save()

            indiki_ay.qiymet = odemek_istediyi_mebleg
            indiki_ay.natamam_ay_alt_status = "NATAMAM NÖVBƏTİ AY"
            indiki_ay.odenme_status = "ÖDƏNƏN"
            # indiki_ay.qeyd = qeyd
            indiki_ay.save()
            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        if(natamama_gore_odeme_status == "NATAMAM SONUNCU AY"):
            indiki_ay = self.get_object()
            natamam_odemek_istediyi_mebleg = indiki_ay.qiymet - odemek_istediyi_mebleg

            sonuncu_ay = odenmeyen_odemetarixler[len(odenmeyen_odemetarixler)-1]
            sonuncu_ay.qiymet = sonuncu_ay.qiymet + natamam_odemek_istediyi_mebleg
            sonuncu_ay.save()

            indiki_ay.qiymet = odemek_istediyi_mebleg
            indiki_ay.natamam_ay_alt_status = "NATAMAM SONUNCU AY"
            indiki_ay.odenme_status = "ÖDƏNƏN"
            # indiki_ay.qeyd = qeyd
            indiki_ay.save()
            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        
    # Buraxilmis Ay odeme statusu ile bagli emeliyyatlar
    if((sertli_odeme_status == "BURAXILMIŞ AY" and sifira_gore_odeme_status != None) or (float(odemek_istediyi_mebleg) == 0 and sifira_gore_odeme_status != None)):
        indiki_ay = self.get_object()
        muqavile = indiki_ay.muqavile
        ilkin_odenis = muqavile.ilkin_odenis
        ilkin_odenis_qaliq = muqavile.ilkin_odenis_qaliq
        mehsulun_qiymeti = muqavile.muqavile_umumi_mebleg
        ilkin_odenis_tam = ilkin_odenis + ilkin_odenis_qaliq
        # indiki_ay.sertli_odeme_status = "BURAXILMIŞ AY"
        # indiki_ay.save()
        odenmeyen_odemetarixler = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)
        odemek_istediyi_mebleg = float(request.data.get("qiymet"))
        
        if(sifira_gore_odeme_status == "SIFIR NÖVBƏTİ AY"):
            novbeti_ay = get_object_or_404(OdemeTarix, pk=self.get_object().id+1)
            novbeti_ay.qiymet = novbeti_ay.qiymet + indiki_ay.qiymet
            novbeti_ay.save()
            indiki_ay.qiymet = 0
            indiki_ay.sertli_odeme_status = "BURAXILMIŞ AY"
            indiki_ay.buraxilmis_ay_alt_status = "SIFIR NÖVBƏTİ AY"
            # indiki_ay.qeyd = qeyd
            indiki_ay.save()
            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        elif(sifira_gore_odeme_status == "SIFIR SONUNCU AY"):
            sonuncu_ay = odenmeyen_odemetarixler[len(odenmeyen_odemetarixler)-1]
            sonuncu_ay.qiymet = sonuncu_ay.qiymet + indiki_ay.qiymet
            sonuncu_ay.save()
            indiki_ay.qiymet = 0
            indiki_ay.sertli_odeme_status = "BURAXILMIŞ AY"
            indiki_ay.buraxilmis_ay_alt_status = "SIFIR SONUNCU AY"
            # indiki_ay.qeyd = qeyd
            indiki_ay.save()
            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        elif(sifira_gore_odeme_status == "SIFIR DİGƏR AYLAR"):
            odenmeyen_pul = indiki_ay.qiymet
            buraxilmamis_odenmeyen_odemetarixler = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)
            odenmeyen_aylar = len(buraxilmamis_odenmeyen_odemetarixler)
            aylara_elave_olunacaq_mebleg = odenmeyen_pul // (odenmeyen_aylar - 1)
            a = aylara_elave_olunacaq_mebleg * ((odenmeyen_aylar - 1)-1)
            sonuncu_aya_elave_olunacaq_mebleg = odenmeyen_pul - a
            indiki_ay.qiymet = 0
            indiki_ay.sertli_odeme_status = "BURAXILMIŞ AY"
            indiki_ay.buraxilmis_ay_alt_status = "SIFIR DİGƏR AYLAR"
            # indiki_ay.qeyd = qeyd
            indiki_ay.save()
            i = 0
            
            while(i<=(odenmeyen_aylar-1)):
                if(indiki_ay == buraxilmamis_odenmeyen_odemetarixler[i]):
                    i+=1
                    continue
                if(i == (odenmeyen_aylar-1)):
                    buraxilmamis_odenmeyen_odemetarixler[i].qiymet = buraxilmamis_odenmeyen_odemetarixler[i].qiymet + sonuncu_aya_elave_olunacaq_mebleg
                    buraxilmamis_odenmeyen_odemetarixler[i].save()
                else:
                    buraxilmamis_odenmeyen_odemetarixler[i].qiymet = buraxilmamis_odenmeyen_odemetarixler[i].qiymet + aylara_elave_olunacaq_mebleg
                    buraxilmamis_odenmeyen_odemetarixler[i].save()
                i+=1
            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)

        pdf_create_when_muqavile_updated(muqavile, muqavile, True)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)

    # RAZILASDIRILMIS AZ ODEME ile bagli emeliyyatlar
    if(sertli_odeme_status == "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ"):
        odemek_istediyi_mebleg = float(request.data.get("qiymet"))
        if float(indiki_ay.qiymet) <= float(odemek_istediyi_mebleg):
            return Response({"detail": "Razılaşdırılmış ödəmə statusunda ödənmək istənilən məbləğ əvvəlki məbləğdən az olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            indiki_ay = self.get_object()
            muqavile = indiki_ay.muqavile
            buraxilmamis_odenmeyen_odemetarixler = OdemeTarix.objects.filter(
                muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", buraxilmis_ay_alt_status=None, sertli_odeme_status=None 
                )
            ilkin_odenis = muqavile.ilkin_odenis
            ilkin_odenis_qaliq = muqavile.ilkin_odenis_qaliq
            ilkin_odenis_tam = ilkin_odenis + ilkin_odenis_qaliq
            mehsulun_qiymeti = muqavile.muqavile_umumi_mebleg
            indiki_ay.sertli_odeme_status = "RAZILAŞDIRILMIŞ AZ ÖDƏMƏ"
            # indiki_ay.qeyd = qeyd
            indiki_ay.save()

            # odenmeyen_odemetarixler = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")
        
            odenmeyen_pul = indiki_ay.qiymet - odemek_istediyi_mebleg
            odenmeyen_aylar = len(buraxilmamis_odenmeyen_odemetarixler)
            
            try:
                aylara_elave_olunacaq_mebleg = odenmeyen_pul // (odenmeyen_aylar - 1)
            except ZeroDivisionError:
                aylara_elave_olunacaq_mebleg = odenmeyen_pul // odenmeyen_aylar
            if(indiki_ay.odenme_status=="ÖDƏNƏN"):
                b = aylara_elave_olunacaq_mebleg * ((odenmeyen_aylar-1)-1)
            elif(indiki_ay.odenme_status=="ÖDƏNMƏYƏN"):
                b = aylara_elave_olunacaq_mebleg * ((odenmeyen_aylar)-1)
            sonuncu_aya_elave_olunacaq_mebleg = odenmeyen_pul - b
            
            indiki_ay.odenme_status = "ÖDƏNMƏYƏN"
            indiki_ay.qiymet = odemek_istediyi_mebleg
            indiki_ay.save()

            qaliq_borc = float(qaliq_borc) - float(indiki_ay.qiymet)
            # muqavile.qaliq_borc = qaliq_borc
            muqavile.save()

            i = 0
            while(i<=(odenmeyen_aylar-1)):
                if(indiki_ay == buraxilmamis_odenmeyen_odemetarixler[i]):
                    i+=1
                    continue
                if(i == (odenmeyen_aylar-1)):
                    buraxilmamis_odenmeyen_odemetarixler[i].qiymet = buraxilmamis_odenmeyen_odemetarixler[i].qiymet + sonuncu_aya_elave_olunacaq_mebleg
                    buraxilmamis_odenmeyen_odemetarixler[i].save()
                else:
                    buraxilmamis_odenmeyen_odemetarixler[i].qiymet = buraxilmamis_odenmeyen_odemetarixler[i].qiymet + aylara_elave_olunacaq_mebleg
                    buraxilmamis_odenmeyen_odemetarixler[i].save()
                i+=1
            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)

    # ARTIQ ODEME ile bagli emeliyyatlar
    if(sertli_odeme_status == "ARTIQ ÖDƏMƏ"):
        odenmek_istenilen_mebleg = request.data.get("qiymet")
        
        if float(indiki_ay.qiymet) >= float(odenmek_istenilen_mebleg):
            return Response({"detail": "Artıq ödəmə statusunda ödənmək istənilən məbləğ əvvəlki məbləğdən çox olmalıdır"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if(artiq_odeme_alt_status == "ARTIQ BİR AY"):
                indiki_ay = self.get_object()
                muqavile = indiki_ay.muqavile
                odemek_istediyi_mebleg = float(request.data.get("qiymet"))
                normalda_odenmeli_olan = indiki_ay.qiymet

                if float(odemek_istediyi_mebleg) > float(muqavile.qaliq_borc):
                    return Response({"detail": "Artıq ödəmə statusunda qalıq borcunuzdan artıq məbləğ ödəyə bilməzsiniz"}, status=status.HTTP_400_BAD_REQUEST)

                artiqdan_normalda_odenmeli_olani_cixan_ferq = odemek_istediyi_mebleg - normalda_odenmeli_olan

                odenmeyen_odemetarixler = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")

                indiki_ay.qiymet = odemek_istediyi_mebleg
                # indiki_ay.odenme_status = "ÖDƏNƏN"
                indiki_ay.sertli_odeme_status = "ARTIQ ÖDƏMƏ"
                indiki_ay.artiq_odeme_alt_status = "ARTIQ BİR AY"
                # indiki_ay.qeyd = qeyd
                indiki_ay.save()
                
                
                qaliq_borc = float(qaliq_borc) - float(odemek_istediyi_mebleg)
                # muqavile.qaliq_borc = qaliq_borc
                muqavile.save()

                sonuncu_ay = odenmeyen_odemetarixler[len(odenmeyen_odemetarixler)-1]
                sonuncudan_bir_evvelki_ay = odenmeyen_odemetarixler[len(odenmeyen_odemetarixler)-2]
                
                sonuncu_aydan_qalan = sonuncu_ay.qiymet - artiqdan_normalda_odenmeli_olani_cixan_ferq

                if(sonuncu_ay.qiymet > artiqdan_normalda_odenmeli_olani_cixan_ferq):
                    sonuncu_ay.qiymet = sonuncu_ay.qiymet - artiqdan_normalda_odenmeli_olani_cixan_ferq
                    sonuncu_ay.save()
                elif(sonuncu_ay.qiymet == artiqdan_normalda_odenmeli_olani_cixan_ferq):
                    sonuncu_ay.delete()
                    muqavile.kredit_muddeti = muqavile.kredit_muddeti - 1
                    muqavile.save()
                elif(sonuncu_ay.qiymet < artiqdan_normalda_odenmeli_olani_cixan_ferq):
                    qalan_mebleg = artiqdan_normalda_odenmeli_olani_cixan_ferq - sonuncu_ay.qiymet
                    sonuncu_ay.delete()
                    muqavile.kredit_muddeti = muqavile.kredit_muddeti - 1
                    muqavile.save()
                    if(sonuncudan_bir_evvelki_ay.qiymet > qalan_mebleg):
                        sonuncudan_bir_evvelki_ay.qiymet = sonuncudan_bir_evvelki_ay.qiymet - qalan_mebleg
                        sonuncudan_bir_evvelki_ay.save()
                    if(sonuncudan_bir_evvelki_ay.qiymet == qalan_mebleg):
                        sonuncudan_bir_evvelki_ay.delete()
                        muqavile.kredit_muddeti = muqavile.kredit_muddeti - 1
                        muqavile.save()
                if(request.data.get("odenme_status") == "ÖDƏNƏN"):
                    qaliq_borc = float(qaliq_borc) - float(odemek_istediyi_mebleg)
                    muqavile.qaliq_borc = qaliq_borc
                    muqavile.save()

                    ilkin_balans = holding_umumi_balans_hesabla()
                    print(f"{ilkin_balans=}")
                    ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)
                    
                    qeyd = f"Vanleader - {vanleader.asa}, müştəri - {musteri.asa}, tarix - {today}, ödəniş üslubu - {odenis_uslubu}. kredit ödəməsi"
                    k_medaxil(ofis_kassa, float(odemek_istediyi_mebleg), vanleader, qeyd)

                    indiki_ay.odenme_status = "ÖDƏNƏN"
                    indiki_ay.save()

                    sonraki_balans = holding_umumi_balans_hesabla()
                    print(f"{sonraki_balans=}")
                    ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
                    pul_axini_create(
                        ofis=ofis,
                        shirket=ofis.shirket,
                        aciqlama=qeyd,
                        ilkin_balans=ilkin_balans,
                        sonraki_balans=sonraki_balans,
                        ofis_ilkin_balans=ofis_ilkin_balans,
                        ofis_sonraki_balans=ofis_sonraki_balans,
                        emeliyyat_eden=user,
                        emeliyyat_uslubu="MƏDAXİL",
                        miqdar=float(odemek_istediyi_mebleg)
                    )


                pdf_create_when_muqavile_updated(muqavile, muqavile, True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            elif(artiq_odeme_alt_status == "ARTIQ BÜTÜN AYLAR"):
                indiki_ay = self.get_object()
                muqavile = indiki_ay.muqavile
                odemek_istediyi_mebleg = float(request.data.get("qiymet"))
                print(f"{odemek_istediyi_mebleg=}")
                normalda_odenmeli_olan = indiki_ay.qiymet

                if float(odemek_istediyi_mebleg) > float(muqavile.qaliq_borc):
                    return Response({"detail": "Artıq ödəmə statusunda qalıq borcunuzdan artıq məbləğ ödəyə bilməzsiniz"}, status=status.HTTP_400_BAD_REQUEST)

                ilkin_odenis = muqavile.ilkin_odenis
                ilkin_odenis_qaliq = muqavile.ilkin_odenis_qaliq
                ilkin_odenis_tam = ilkin_odenis + ilkin_odenis_qaliq
                mehsulun_qiymeti = muqavile.muqavile_umumi_mebleg
                odenen_odemetarixler = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status = "ÖDƏNƏN")
                odenmeyen_odemetarixler = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)
                umumi_odenmeyen_odemetarixler = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN").exclude(sertli_odeme_status="BURAXILMIŞ AY")
                sertli_odeme = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN").exclude(sertli_odeme_status=None)
                print(f"******************************{odenmeyen_odemetarixler=} ---> {len(odenmeyen_odemetarixler)}")
                print(f"******************************{umumi_odenmeyen_odemetarixler=} ---> {len(umumi_odenmeyen_odemetarixler)}")
                print(f"******************{sertli_odeme=}")

                sertli_odemeden_gelen_mebleg = 0
                for s in sertli_odeme:
                    sertli_odemeden_gelen_mebleg += float(s.qiymet)
                print(f"******************{sertli_odemeden_gelen_mebleg=}")
                odeme_tarixleri = OdemeTarix.objects.filter(muqavile=muqavile)
                # odediyi = len(odenen_odemetarixler) * indiki_ay.qiymet
                qaliq_borc = float(muqavile.qaliq_borc)
                print(f"******************{qaliq_borc=}")
                yeni_qaliq_borc = qaliq_borc-sertli_odemeden_gelen_mebleg
                print(f"******************{yeni_qaliq_borc=}")
                # cixilacaq_mebleg = qaliq_borc -  sertli_odemeden_gelen_mebleg
                yeni_aylar = yeni_qaliq_borc // odemek_istediyi_mebleg
                print(f"******************{yeni_aylar=}")
                # silinecek_ay = len(odenmeyen_odemetarixler) - yeni_aylar
                silinecek_ay = len(umumi_odenmeyen_odemetarixler) - yeni_aylar - len(sertli_odeme)
                print(f"******************{silinecek_ay=}")
                son_aya_elave_edilecek_mebleg = yeni_qaliq_borc - ((yeni_aylar-1) * odemek_istediyi_mebleg)
                print(f"******************{son_aya_elave_edilecek_mebleg=}")
                indiki_ay.qiymet = odemek_istediyi_mebleg
                # indiki_ay.odenme_status = "ÖDƏNƏN"
                indiki_ay.sertli_odeme_status = "ARTIQ ÖDƏMƏ"
                indiki_ay.artiq_odeme_alt_status = "ARTIQ BÜTÜN AYLAR"
                # indiki_ay.qeyd = qeyd
                indiki_ay.save()

                qaliq_borc = float(qaliq_borc) - float(odemek_istediyi_mebleg)
                # muqavile.qaliq_borc = qaliq_borc
                muqavile.save()

                a = 1
                while(a <= silinecek_ay):
                    odenmeyen_odemetarixler[len(odenmeyen_odemetarixler)-1].delete()
                    odenmeyen_odemetarixler = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)
                    a += 1

                print(f"********Silinmeden sonra***********{odenmeyen_odemetarixler=} ---> {len(odenmeyen_odemetarixler)}")

                b = 0
                if float(odemek_istediyi_mebleg) == float(qaliq_borc):
                    while(b < yeni_aylar):
                        print(f"******************{b=}")
                        odenmeyen_odemetarixler[b].qiymet = odemek_istediyi_mebleg
                        odenmeyen_odemetarixler[b].save()
                        b += 1
                elif float(odemek_istediyi_mebleg) < float(qaliq_borc):
                    while(b < yeni_aylar):
                        print(f"******************{b=}")
                        if(b < yeni_aylar-1):
                            odeme_tarixi = odenmeyen_odemetarixler[b]
                            odeme_tarixi.qiymet = odemek_istediyi_mebleg
                            odeme_tarixi.save()
                            b += 1
                        elif(b == yeni_aylar-1):
                            odenmeyen_odemetarixler[len(odenmeyen_odemetarixler)-1].qiymet = son_aya_elave_edilecek_mebleg
                            odenmeyen_odemetarixler[len(odenmeyen_odemetarixler)-1].save()
                            b += 1
                        
                # serializer.save()
                pdf_create_when_muqavile_updated(muqavile, muqavile, True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    
    # SON AYIN BOLUNMESI
    if(sertli_odeme_status == "SON AYIN BÖLÜNMƏSİ"):
        indiki_ay = self.get_object()
        muqavile = indiki_ay.muqavile
        odemek_istediyi_mebleg = float(request.data.get("qiymet"))

        if float(odemek_istediyi_mebleg) == 0:
            return Response({"detail": "Sonuncu ayda 0 AZN daxil edilə bilməz"}, status=status.HTTP_400_BAD_REQUEST)

        odenmeyen_odemetarixler = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")
        sonuncu_ay = odenmeyen_odemetarixler[len(odenmeyen_odemetarixler)-1]

        try:
            if(indiki_ay != sonuncu_ay):
                raise ValidationError(detail={"detail": "Sonuncu ayda deyilsiniz!"}, code=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail": "Sonuncu ayda deyilsiniz"}, status=status.HTTP_400_BAD_REQUEST) 

        
        create_olunacaq_ay_qiymet = sonuncu_ay.qiymet - odemek_istediyi_mebleg
        sonuncu_ay.qiymet = odemek_istediyi_mebleg
        # sonuncu_ay.odenme_status = "ÖDƏNƏN"
        sonuncu_ay.sertli_odeme_status = "SON AYIN BÖLÜNMƏSİ"
        sonuncu_ay.qeyd = qeyd
        sonuncu_ay.save()

        qaliq_borc = float(qaliq_borc) - float(odemek_istediyi_mebleg)
        # muqavile.qaliq_borc = qaliq_borc
        muqavile.save()

        inc_month = pd.date_range(sonuncu_ay.tarix, periods = 2, freq='M')
        OdemeTarix.objects.create(
            ay_no = int(sonuncu_ay.ay_no) + 1,
            muqavile = muqavile,
            tarix = f"{inc_month[1].year}-{inc_month[1].month}-{sonuncu_ay.tarix.day}",
            qiymet = create_olunacaq_ay_qiymet
        ).save()
        pdf_create_when_muqavile_updated(muqavile, muqavile, True)
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    # Odenen ay ile bagli emeliyyat
    if((indiki_ay.odenme_status == "ÖDƏNMƏYƏN" and float(odemek_istediyi_mebleg) == indiki_ay.qiymet)):
        odenmeyen_odemetarixler_qs = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")
        odenmeyen_odemetarixler = list(odenmeyen_odemetarixler_qs)
        if serializer.is_valid():
            indiki_ay.odenme_status = "ÖDƏNƏN"
            # indiki_ay.qeyd = qeyd
            indiki_ay.save()
            if(indiki_ay == odenmeyen_odemetarixler[-1]):
                muqavile.muqavile_status = "BİTMİŞ"
                muqavile.save()
            
            qaliq_borc = float(qaliq_borc) - float(odemek_istediyi_mebleg)
            muqavile.qaliq_borc = qaliq_borc
            muqavile.save()

            ilkin_balans = holding_umumi_balans_hesabla()
            print(f"{ilkin_balans=}")
            ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)
            
            qeyd = f"Vanleader - {vanleader.asa}, müştəri - {musteri.asa}, tarix - {today}, ödəniş üslubu - {odenis_uslubu}. kredit ödəməsi"
            k_medaxil(ofis_kassa, float(odemek_istediyi_mebleg), vanleader, qeyd)

            sonraki_balans = holding_umumi_balans_hesabla()
            print(f"{sonraki_balans=}")
            ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
            pul_axini_create(
                ofis=ofis,
                shirket=ofis.shirket,
                aciqlama=qeyd,
                ilkin_balans=ilkin_balans,
                sonraki_balans=sonraki_balans,
                ofis_ilkin_balans=ofis_ilkin_balans,
                ofis_sonraki_balans=ofis_sonraki_balans,
                emeliyyat_eden=user,
                emeliyyat_uslubu="MƏDAXİL",
                miqdar=float(odemek_istediyi_mebleg)
            )

            pdf_create_when_muqavile_updated(muqavile, muqavile, True)
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
        else:
            traceback.print_exc()
            return Response({"detail": "Xəta"}, status=status.HTTP_400_BAD_REQUEST)
            # return ValidationError(detail={"detail": "Məlumatları doğru daxil edin"}, code=status.HTTP_400_BAD_REQUEST)
            
    else:
        traceback.print_exc()
        return Response({"detail": "Yanlış əməliyyat"}, status=status.HTTP_400_BAD_REQUEST)