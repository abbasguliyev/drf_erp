import math
from rest_framework import status
from rest_framework.response import Response
from account.models import User, Musteri
from restAPI.v1.contract.serializers import MuqavileSerializer
from company.models import Ofis, Shobe, Vezifeler
from cashbox.models import OfisKassa
from income_expense.models import OfisKassaMedaxil, OfisKassaMexaric
from salary.models import (
    Menecer1Prim, 
    Menecer1PrimNew, 
    MaasGoruntuleme, 
    OfficeLeaderPrim, 
    GroupLeaderPrim, 
    GroupLeaderPrimNew
)
from contract.models import OdemeTarix
from warehouse.models import (
    Anbar,
    Stok
)
from product.models import Mehsullar
from services.models import Servis, ServisOdeme
from rest_framework.generics import get_object_or_404
import pandas as pd
import datetime
import traceback
from services.signals import create_services

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
    ofis_balans_hesabla, 
)

import django

def create_and_add_pdf_when_muqavile_updated(sender, instance, created, **kwargs):
    if created:
        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.ofis.shirket.shirket_adi == okean:
            muqavile_pdf_canvas_list = okean_muqavile_pdf_canvas(
                muqavile=instance, musteri=instance.musteri
            )
            muqavile_pdf = okean_create_muqavile_pdf(
                muqavile_pdf_canvas_list, instance)
        elif instance.ofis.shirket.shirket_adi == magnus:
            muqavile_pdf_canvas_list = magnus_muqavile_pdf_canvas(
                muqavile=instance, musteri=instance.musteri
            )
            muqavile_pdf = magnus_create_muqavile_pdf(
                muqavile_pdf_canvas_list, instance)
        instance.pdf = muqavile_pdf
        instance.save()


def create_and_add_pdf_when_muqavile_kredit_updated(sender, instance, created, **kwargs):
    if created:
        okean = "OCEAN"
        magnus = "MAGNUS"

        if instance.ofis.shirket.shirket_adi == okean:
            muqavile_pdf_canvas_list = ocean_kredit_muqavile_pdf_canvas(
                muqavile=instance
            )
            muqavile_pdf = ocean_kredit_create_muqavile_pdf(
                muqavile_pdf_canvas_list, instance)
        elif instance.ofis.shirket.shirket_adi == magnus:
            muqavile_pdf_canvas_list = magnus_kredit_muqavile_pdf_canvas(
                muqavile=instance
            )
            muqavile_pdf = magnus_kredit_create_muqavile_pdf(
                muqavile_pdf_canvas_list, instance)
        instance.pdf_elave = muqavile_pdf
        instance.save()


def pdf_create_when_muqavile_updated(sender, instance, created):
    create_and_add_pdf_when_muqavile_updated(
        sender=sender, instance=instance, created=created)
    create_and_add_pdf_when_muqavile_kredit_updated(
        sender=sender, instance=instance, created=created)
# ----------------------------------------------------------------------------------------------------------------------


def stok_mehsul_ciximi(stok, mehsul_sayi):
    stok.say = stok.say - int(mehsul_sayi)
    stok.save()
    if (stok.say == 0):
        stok.delete()
    return stok.say


def stok_mehsul_elave(stok, mehsul_sayi):
    stok.say = stok.say + int(mehsul_sayi)
    stok.save()
    return stok.say


def k_medaxil(company_kassa, daxil_edilecek_mebleg, group_leader, qeyd):
    yekun_balans = float(daxil_edilecek_mebleg) + float(company_kassa.balans)
    company_kassa.balans = yekun_balans
    company_kassa.save()
    tarix = datetime.date.today()

    medaxil = OfisKassaMedaxil.objects.create(
        medaxil_eden=group_leader,
        ofis_kassa=company_kassa,
        mebleg=daxil_edilecek_mebleg,
        medaxil_tarixi=tarix,
        qeyd=qeyd
    )
    medaxil.save()
    return medaxil


def k_mexaric(company_kassa, daxil_edilecek_mebleg, group_leader, qeyd):
    yekun_balans = float(company_kassa.balans) - float(daxil_edilecek_mebleg)
    company_kassa.balans = yekun_balans
    company_kassa.save()
    tarix = datetime.date.today()

    mexaric = OfisKassaMexaric.objects.create(
        mexaric_eden=group_leader,
        ofis_kassa=company_kassa,
        mebleg=daxil_edilecek_mebleg,
        mexaric_tarixi=tarix,
        qeyd=qeyd
    )
    mexaric.save()
    return mexaric

# ----------------------------------------------------------------------------------------------------------------------


def create_odeme_tarix_when_update_muqavile(
    instance, kredit_muddeti, odenis_uslubu, ilkin_odenis, ilkin_odenis_qaliq,  **kwargs
):
    """
    Bu method ne zaman muqavile negd odenisden kredite kecirilerse o zaman ishe dushur.
    """

    kredit_muddeti = kredit_muddeti
    mehsul_sayi = instance.mehsul_sayi

    def kredit_muddeti_func(kredit_muddeti, mehsul_sayi):
        kredit_muddeti_yeni = kredit_muddeti * mehsul_sayi
        return kredit_muddeti_yeni

    if(odenis_uslubu == "KREDİT"):

        indi = datetime.datetime.today().strftime('%d-%m-%Y')
        inc_month = pd.date_range(indi, periods=kredit_muddeti+1, freq='M')

        ilkin_odenis = ilkin_odenis
        ilkin_odenis_qaliq = ilkin_odenis_qaliq

        if(ilkin_odenis is not None):
            ilkin_odenis = float(ilkin_odenis)

        if(ilkin_odenis_qaliq is not None):
            ilkin_odenis_qaliq = float(ilkin_odenis_qaliq)

        mehsulun_qiymeti = instance.muqavile_umumi_mebleg

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
            while(i <= kredit_muddeti):
                if(i == kredit_muddeti):
                    if(datetime.date.today().day < 29):
                        OdemeTarix.objects.create(
                            ay_no=i,
                            muqavile=instance,
                            tarix=f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}",
                            qiymet=son_aya_odenecek_mebleg
                        ).save()
                    elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                        if(inc_month[i].day <= datetime.date.today().day):
                            OdemeTarix.objects.create(
                                ay_no=i,
                                muqavile=instance,
                                tarix=f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                                qiymet=son_aya_odenecek_mebleg
                            ).save()
                        else:
                            OdemeTarix.objects.create(
                                ay_no=i,
                                muqavile=instance,
                                tarix=f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}",
                                qiymet=son_aya_odenecek_mebleg,
                                sonuncu_ay=True
                            ).save()
                else:
                    if(datetime.date.today().day < 29):
                        OdemeTarix.objects.create(
                            ay_no=i,
                            muqavile=instance,
                            tarix=f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}",
                            qiymet=aylara_gore_odenecek_mebleg
                        ).save()
                    elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                        if(inc_month[i].day <= datetime.date.today().day):
                            OdemeTarix.objects.create(
                                ay_no=i,
                                muqavile=instance,
                                tarix=f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                                qiymet=aylara_gore_odenecek_mebleg
                            ).save()
                        else:
                            OdemeTarix.objects.create(
                                ay_no=i,
                                muqavile=instance,
                                tarix=f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}",
                                qiymet=aylara_gore_odenecek_mebleg
                            ).save()
                i += 1


def muqavile_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    user = None

    group_leader_id = request.data.get("group_leader_id")

    if (group_leader_id == None):
        user = self.request.user
    else:
        user = get_object_or_404(User, pk=group_leader_id)

    menecer1_id = request.data.get("menecer1_id")
    menecer2_id = request.data.get("menecer2_id")

    musteri_id = request.data.get("musteri_id")
    if musteri_id == None:
        return Response({"detail": "Müştəri qeyd olunmayıb"}, status=status.HTTP_400_BAD_REQUEST)
    musteri = get_object_or_404(Musteri, pk=musteri_id)

    menecer1 = None
    menecer2 = None

    if (menecer1_id is not None):
        try:
            menecer1 = get_object_or_404(User, pk=menecer1_id)
            if (menecer2_id == None):
                menecer2 = menecer1
        except:
            return Response({"detail": "Menecer1 tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    if (menecer2_id is not None):
        try:
            menecer2 = get_object_or_404(User, pk=menecer2_id)
            if (menecer1_id == None):
                menecer1 = menecer2
        except:
            return Response({"detail": "Menecer2 tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    my_time = datetime.datetime.min.time()

    indiki_tarix_date = datetime.date.today()
    indiki_tarix = datetime.datetime.combine(indiki_tarix_date, my_time)
    indiki_tarix_san = datetime.datetime.timestamp(indiki_tarix)

    if (request.data.get("ilkin_odenis_tarixi") is not None):
        ilkin_odenis_tarixi = request.data.get("ilkin_odenis_tarixi")
        ilkin_odenis_tarixi_date = datetime.datetime.strptime(
            ilkin_odenis_tarixi, "%d-%m-%Y")
        ilkin_odenis_tarixi_san = datetime.datetime.timestamp(
            ilkin_odenis_tarixi_date)

    if (request.data.get("ilkin_odenis_qaliq_tarixi") is not None):
        ilkin_odenis_qaliq_tarixi = request.data.get(
            "ilkin_odenis_qaliq_tarixi")
        ilkin_odenis_qaliq_tarixi_date = datetime.datetime.strptime(
            ilkin_odenis_qaliq_tarixi, "%d-%m-%Y")
        ilkin_odenis_qaliq_tarixi_san = datetime.datetime.timestamp(
            ilkin_odenis_qaliq_tarixi_date)

    mehsul_id_str = request.data.get("mehsul_id")
    if (mehsul_id_str == None):
        return Response({"detail": "Müqavilə imzalamaq üçün mütləq məhsul daxil edilməlidir."},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        mehsul_id = int(mehsul_id_str)

    try:
        mehsul = get_object_or_404(Mehsullar, pk=mehsul_id)
    except:
        return Response({"detail": "Məhsul tapılmadı"},
                        status=status.HTTP_400_BAD_REQUEST)

    mehsul_sayi = request.data.get("mehsul_sayi")
    if (mehsul_sayi == None):
        mehsul_sayi = 1

    odenis_uslubu = request.data.get("odenis_uslubu")

    ilkin_odenis = request.data.get("ilkin_odenis")

    ilkin_odenis_qaliq = request.data.get("ilkin_odenis_qaliq")

    def umumi_mebleg(mehsul_qiymeti, mehsul_sayi):
        muqavile_umumi_mebleg = mehsul_qiymeti * mehsul_sayi
        return muqavile_umumi_mebleg

    if (mehsul_sayi == None):
        mehsul_sayi = 1

    muqavile_umumi_mebleg = umumi_mebleg(mehsul.qiymet, int(mehsul_sayi))

    ofis_id = request.data.get("ofis_id")

    shirket_id = request.data.get("shirket_id")

    kredit_muddeti = request.data.get("kredit_muddeti")

    if (user.ofis == None):
        ofis = Ofis.objects.get(pk=ofis_id)
    else:
        ofis = user.ofis
    if (user.shirket == None):
        shirket = mehsul.shirket
    else:
        shirket = user.shirket

    try:
        anbar = get_object_or_404(Anbar, ofis=ofis)
    except:
        traceback.print_exc()
        return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ofis_kassa = get_object_or_404(OfisKassa, ofis=ofis)
    except:
        traceback.print_exc()
        return Response({"detail": "Ofis Kassa tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    ofis_kassa_balans = ofis_kassa.balans
    qaliq_borc = 0

    try:
        try:
            stok = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)
        except:
            return Response({"detail": "Stokda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)
        if (stok.say < int(mehsul_sayi)):
            return Response({"detail": "Stokda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

        if (serializer.is_valid()):
            if (mehsul_sayi == None):
                mehsul_sayi = 1
            # Kredit
            if (odenis_uslubu == "KREDİT"):
                if (kredit_muddeti == None):
                    # Kredit muddeti daxil edilmezse
                    return Response({"detail": "Ödəmə statusu kreditdir amma kredit müddəti daxil edilməyib"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif (int(kredit_muddeti) == 0):
                    # Kredit muddeyi 0 daxil edilerse
                    return Response({"detail": "Ödəmə statusu kreditdir amma kredit müddəti 0 daxil edilib"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif (int(kredit_muddeti) > 30):
                    # Kredit muddeti 31 ay daxil edilerse
                    return Response({"detail": "Maksimum kredit müddəti 30 aydır"}, status=status.HTTP_400_BAD_REQUEST)
                elif (int(kredit_muddeti) > 0):
                    # Kredit muddeti 0-dan boyuk olarsa

                    if ((ilkin_odenis is not None) and (request.data.get("ilkin_odenis_tarixi") == None)):
                        ilkin_odenis_tarixi = indiki_tarix_date
                        ilkin_odenis_tarixi_date = indiki_tarix
                        ilkin_odenis_tarixi_san = indiki_tarix_san

                    if ((ilkin_odenis_qaliq is not None) and (request.data.get("ilkin_odenis_qaliq_tarixi") == None)):
                        return Response({
                            "detail": "Qalıq İlkin ödəniş məbləği qeyd olunub amma qalıq ilkin ödəniş tarixi qeyd olunmayıb"},
                            status=status.HTTP_400_BAD_REQUEST)

                    if (ilkin_odenis == None and ilkin_odenis_qaliq == None):
                        # Ilkin odenis daxil edilmezse
                        stok_mehsul_ciximi(stok, int(mehsul_sayi))
                        muqavile_umumi_mebleg = umumi_mebleg(
                            mehsul.qiymet, int(mehsul_sayi))

                        qaliq_borc = float(muqavile_umumi_mebleg)

                        serializer.save(group_leader=user, menecer1=menecer1, menecer2=menecer2, shirket=shirket, ofis=ofis,
                                        muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc)
                        # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                        #                 status=status.HTTP_201_CREATED)
                        return Response(data=serializer.data,
                                        status=status.HTTP_201_CREATED)
                    elif (ilkin_odenis is not None and ilkin_odenis_qaliq == None):
                        muqavile_umumi_mebleg = umumi_mebleg(mehsul.qiymet, int(mehsul_sayi))
                        if float(ilkin_odenis) >= float(muqavile_umumi_mebleg):
                            return Response({"detail": "İlkin ödəniş məbləği müqavilənin məbləğindən çox ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
                        # Umumi ilkin odenis meblegi daxil edilerse ve qaliq ilkin odenis meblegi daxil edilmezse
                        if (indiki_tarix_san == ilkin_odenis_tarixi_san):
                            stok_mehsul_ciximi(stok, int(mehsul_sayi))
                            muqavile_umumi_mebleg = umumi_mebleg(mehsul.qiymet, int(mehsul_sayi))
                            
                            ilkin_balans = holding_umumi_balans_hesabla()
                            ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)
                            qeyd = f"GroupLeader - {user.asa}, müştəri - {musteri.asa}, tarix - {ilkin_odenis_tarixi}, ödəniş üslubu - {odenis_uslubu}, tam ilkin ödəniş"
                            k_medaxil(ofis_kassa, float(
                                ilkin_odenis), user, qeyd)

                            qaliq_borc = float(
                                muqavile_umumi_mebleg) - float(ilkin_odenis)
                            serializer.save(group_leader=user, menecer1=menecer1, menecer2=menecer2, shirket=shirket,
                                            ofis=ofis, ilkin_odenis=ilkin_odenis,
                                            ilkin_odenis_status="BİTMİŞ", muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc,)
                            sonraki_balans = holding_umumi_balans_hesabla()
                            ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
                            pul_axini_create(
                                ofis=ofis,
                                shirket=ofis.shirket,
                                aciqlama=f"GroupLeader - {user.asa}, müştəri - {musteri.asa}, tarix - {ilkin_odenis_tarixi}, ödəniş üslubu - {odenis_uslubu}, tam ilkin ödəniş",
                                ilkin_balans=ilkin_balans,
                                sonraki_balans=sonraki_balans,
                                ofis_ilkin_balans=ofis_ilkin_balans,
                                ofis_sonraki_balans=ofis_sonraki_balans,
                                emeliyyat_eden=user,
                                emeliyyat_uslubu="MƏDAXİL",
                                miqdar=float(ilkin_odenis)
                            )
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)
                        elif (indiki_tarix_san < ilkin_odenis_tarixi_san):
                            stok_mehsul_ciximi(stok, int(mehsul_sayi))
                            muqavile_umumi_mebleg = umumi_mebleg(
                                mehsul.qiymet, int(mehsul_sayi))

                            qaliq_borc = float(
                                muqavile_umumi_mebleg) - float(ilkin_odenis)

                            serializer.save(group_leader=user, menecer1=menecer1, menecer2=menecer2, shirket=shirket,
                                            ofis=ofis, ilkin_odenis=ilkin_odenis,
                                            ilkin_odenis_status="DAVAM EDƏN", qaliq_borc=qaliq_borc,
                                            muqavile_umumi_mebleg=muqavile_umumi_mebleg)
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)
                        elif (indiki_tarix_san > ilkin_odenis_tarixi_san):
                            return Response({"detail": "İlkin ödəniş tarixini keçmiş tarixə təyin edə bilməzsiniz"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                        #                 status=status.HTTP_201_CREATED)
                        return Response(data=serializer.data,
                                        status=status.HTTP_201_CREATED)

                    elif ((ilkin_odenis == None and ilkin_odenis_qaliq is not None) or (
                            float(ilkin_odenis) == 0 and ilkin_odenis_qaliq is not None)):
                        return Response({"detail": "İlkin ödəniş daxil edilmədən qalıq ilkin ödəniş daxil edilə bilməz"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    elif (float(ilkin_odenis) == 0):
                        # Umumi ilkin odenis meblegi 0 olarsa
                        return Response({"detail": "İlkin ödəniş 0 azn daxil edilə bilməz"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    elif (ilkin_odenis_qaliq is not None):
                        muqavile_umumi_mebleg2 = umumi_mebleg(mehsul.qiymet, int(mehsul_sayi))
                        qaliq_borc2 = float(muqavile_umumi_mebleg2) - float(ilkin_odenis_qaliq)
                        if float(ilkin_odenis) >= float(qaliq_borc2):
                            return Response({"detail": "İlkin ödəniş qalıq məbləği qalıq məbləğdən çox ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
                        if ((indiki_tarix_san == ilkin_odenis_tarixi_san) and (
                                indiki_tarix_san < ilkin_odenis_qaliq_tarixi_san)):
                            stok_mehsul_ciximi(stok, int(mehsul_sayi))
                            muqavile_umumi_mebleg = umumi_mebleg(
                                mehsul.qiymet, int(mehsul_sayi))

                            ilkin_balans = holding_umumi_balans_hesabla()
                            ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

                            qeyd = f"GroupLeader - {user.asa}, müştəri - {musteri.asa}, tarix - {ilkin_odenis_tarixi}, ödəniş üslubu - {odenis_uslubu}, 2-dəfəyə ilkin ödənişin birincisi."
                            k_medaxil(ofis_kassa, float(
                                ilkin_odenis), user, qeyd)

                            qaliq_borc = float(muqavile_umumi_mebleg) - float(ilkin_odenis)

                            serializer.save(group_leader=user, menecer1=menecer1, menecer2=menecer2, shirket=shirket,
                                            ofis=ofis, ilkin_odenis=ilkin_odenis,
                                            ilkin_odenis_qaliq=ilkin_odenis_qaliq, ilkin_odenis_status="BİTMİŞ",
                                            qaliq_ilkin_odenis_status="DAVAM EDƏN",
                                            muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc)
                            sonraki_balans = holding_umumi_balans_hesabla()
                            ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
                            pul_axini_create(
                                ofis=ofis,
                                shirket=ofis.shirket,
                                aciqlama=f"GroupLeader - {user.asa}, müştəri - {musteri.asa}, tarix - {ilkin_odenis_tarixi}, ödəniş üslubu - {odenis_uslubu}, 2-dəfəyə ilkin ödənişin birincisi.",
                                ilkin_balans=ilkin_balans,
                                sonraki_balans=sonraki_balans,
                                ofis_ilkin_balans=ofis_ilkin_balans,
                                ofis_sonraki_balans=ofis_sonraki_balans,
                                emeliyyat_eden=user,
                                emeliyyat_uslubu="MƏDAXİL",
                                miqdar=float(ilkin_odenis)
                            )
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)

                        elif ((indiki_tarix_san == ilkin_odenis_tarixi_san) and (
                                ilkin_odenis_tarixi_san == ilkin_odenis_qaliq_tarixi_san)):
                            return Response({
                                "detail": "İlkin ödəniş qalıq və ilkin ödəniş hər ikisi bu günki tarixə qeyd oluna bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
                        elif (indiki_tarix_san == ilkin_odenis_qaliq_tarixi_san):
                            return Response({"detail": "İlkin ödəniş qalıq bu günki tarixə qeyd oluna bilməz"},
                                            status=status.HTTP_400_BAD_REQUEST)
                        elif (ilkin_odenis_tarixi_san > ilkin_odenis_qaliq_tarixi_san):
                            return Response(
                                {"detail": "İlkin ödəniş qalıq tarixi ilkin ödəniş tarixindən əvvəl ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
                        elif (ilkin_odenis_tarixi_san == ilkin_odenis_qaliq_tarixi_san):
                            return Response({
                                "detail": "İlkin ödəniş qalıq və ilkin ödəniş hər ikisi eyni tarixə qeyd oluna bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)
                        elif ((indiki_tarix_san > ilkin_odenis_tarixi_san) or (
                                indiki_tarix_san > ilkin_odenis_qaliq_tarixi_san)):
                            return Response({"detail": "İlkin ödəniş tarixini keçmiş tarixə təyin edə bilməzsiniz"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        elif (indiki_tarix_san < ilkin_odenis_tarixi_san):
                            stok_mehsul_ciximi(stok, int(mehsul_sayi))
                            muqavile_umumi_mebleg = umumi_mebleg(
                                mehsul.qiymet, int(mehsul_sayi))

                            # qaliq_borc = float(muqavile_umumi_mebleg) - float(ilkin_odenis_qaliq) - float(ilkin_odenis)
                            qaliq_borc = float(muqavile_umumi_mebleg)

                            serializer.save(group_leader=user, menecer1=menecer1, menecer2=menecer2, shirket=shirket,
                                            ofis=ofis, ilkin_odenis=ilkin_odenis,
                                            ilkin_odenis_qaliq=ilkin_odenis_qaliq, ilkin_odenis_status="DAVAM EDƏN",
                                            qaliq_ilkin_odenis_status="DAVAM EDƏN",
                                            muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc)
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)
                        elif ((indiki_tarix_san < ilkin_odenis_tarixi_san) and (
                                indiki_tarix_san < ilkin_odenis_qaliq_tarixi_san)):
                            stok_mehsul_ciximi(stok, int(mehsul_sayi))
                            muqavile_umumi_mebleg = umumi_mebleg(
                                mehsul.qiymet, int(mehsul_sayi))

                            # qaliq_borc = float(muqavile_umumi_mebleg) - float(ilkin_odenis_qaliq) - float(ilkin_odenis)
                            qaliq_borc = float(muqavile_umumi_mebleg)

                            serializer.save(group_leader=user, menecer1=menecer1, menecer2=menecer2, shirket=shirket,
                                            ofis=ofis, ilkin_odenis=ilkin_odenis,
                                            ilkin_odenis_qaliq=ilkin_odenis_qaliq, ilkin_odenis_status="DAVAM EDƏN",
                                            qaliq_ilkin_odenis_status="DAVAM EDƏN",
                                            muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc)
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data,
                                            status=status.HTTP_201_CREATED)

                        # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                        #                 status=status.HTTP_201_CREATED)
                        return Response(data=serializer.data,
                                        status=status.HTTP_201_CREATED)
                    else:
                        return Response({"detail": "Qalıq ilkin ödəniş doğru daxil edilməyib."},
                                        status=status.HTTP_400_BAD_REQUEST)

            # Negd odenis
            elif (odenis_uslubu == "NƏĞD"):
                if (kredit_muddeti is not None):
                    return Response({"detail": "Kredit müddəti ancaq status kredit olan müqavilələr üçündür"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if (ilkin_odenis is not None or ilkin_odenis_qaliq is not None):
                    return Response({"detail": "İlkin ödəniş ancaq status kredit olan müqavilələr üçündür"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if (mehsul_sayi == None):
                    mehsul_sayi = 1

                stok_mehsul_ciximi(stok, int(mehsul_sayi))
                muqavile_umumi_mebleg = umumi_mebleg(
                    mehsul.qiymet, int(mehsul_sayi))

                ilkin_balans = holding_umumi_balans_hesabla()
                ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

                qeyd = f"GroupLeader - {user.asa}, müştəri - {musteri.asa}, tarix - {indiki_tarix_date}, ödəniş üslubu - {odenis_uslubu}"
                k_medaxil(ofis_kassa, float(muqavile_umumi_mebleg), user, qeyd)

                serializer.save(group_leader=user, menecer1=menecer1, menecer2=menecer2, shirket=shirket, ofis=ofis,
                                muqavile_status="BİTMİŞ", muqavile_umumi_mebleg=muqavile_umumi_mebleg)

                sonraki_balans = holding_umumi_balans_hesabla()
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
                    miqdar=float(muqavile_umumi_mebleg)
                )
                # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"}, status=status.HTTP_201_CREATED)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        traceback.print_exc()
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)

def muqavile_update(self, request, *args, **kwargs):
    try:
        muqavile = self.get_object()
        serializer = self.get_serializer(muqavile, data=request.data, partial=True)
        # serializer = MuqavileSerializer(muqavile, data=request.data, partial=True)
        ilkin_odenis = muqavile.ilkin_odenis
        ilkin_odenis_qaliq = muqavile.ilkin_odenis_qaliq
        ilkin_odenis_status = muqavile.ilkin_odenis_status
        qaliq_ilkin_odenis_status = muqavile.qaliq_ilkin_odenis_status
        odemek_istediyi_ilkin_odenis = request.data.get("ilkin_odenis")
        odemek_istediyi_qaliq_ilkin_odenis = request.data.get(
            "ilkin_odenis_qaliq")

        muqavile_status = muqavile.muqavile_status
        my_time = datetime.datetime.min.time()

        indiki_tarix_date = datetime.date.today()
        indiki_tarix = datetime.datetime.combine(indiki_tarix_date, my_time)
        indiki_tarix_san = datetime.datetime.timestamp(indiki_tarix)
        dusen_muqavile_status = request.data.get("muqavile_status")
        mehsul = muqavile.mehsul
        mehsul_sayi = muqavile.mehsul_sayi
        muqavile_group_leader = muqavile.group_leader
        ofis=muqavile.ofis
        musteri = muqavile.musteri
        musteri_id = request.data.get("musteri_id")
        if (musteri_id is not None):
            musteri = get_object_or_404(Musteri, pk=musteri_id)

        muqavile_menecer1 = muqavile.menecer1
        yeni_qrafik = request.data.get("yeni_qrafik_status")
        # YENI QRAFIK ile bagli emeliyyatlar
        if(yeni_qrafik == "YENİ QRAFİK"):
            ilkin_odenis = muqavile.ilkin_odenis
            ilkin_odenis_qaliq = muqavile.ilkin_odenis_qaliq
            ilkin_odenis_tam = ilkin_odenis + ilkin_odenis_qaliq
            mehsulun_qiymeti = muqavile.muqavile_umumi_mebleg
            odenen_odemetarixler = OdemeTarix.objects.filter(
                muqavile=muqavile, odenme_status="ÖDƏNƏN")

            odenmeyen_odemetarixler = OdemeTarix.objects.filter(
                muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)

            sertli_odeme = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN").exclude(sertli_odeme_status=None)

            odenmeyen_odemetarixi_mebleg = OdemeTarix.objects.filter(muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN", sertli_odeme_status=None)[0].qiymet

            odemek_istediyi_mebleg = float(
                request.data.get("yeni_qrafik_mebleg"))

            if odemek_istediyi_mebleg < odenmeyen_odemetarixi_mebleg:
                odenen_mebleg = 0
                for i in odenen_odemetarixler:
                    odenen_mebleg += float(i.qiymet)

                sertli_odemeden_gelen_mebleg = 0
                for s in sertli_odeme:
                    sertli_odemeden_gelen_mebleg += float(s.qiymet)
                odediyi = float(odenen_mebleg) + ilkin_odenis_tam
                qaliq_borc = mehsulun_qiymeti - odediyi
                cixilacaq_mebleg = qaliq_borc -  sertli_odemeden_gelen_mebleg

                odenmeyen_aylar = len(odenmeyen_odemetarixler)
                try:
                    elave_olunacaq_ay_qaliqli = cixilacaq_mebleg / odemek_istediyi_mebleg
                    # muqavile.yeni_qrafik_status = "YENİ QRAFİK"
                    muqavile.qaliq_borc = qaliq_borc
                    muqavile.save()
                except:
                    return Response({"detail": "Ödəmək istədiyiniz məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

                elave_olunacaq_ay = math.ceil(elave_olunacaq_ay_qaliqli)
                create_olunacaq_ay = elave_olunacaq_ay - len(odenmeyen_odemetarixler)
                a = odemek_istediyi_mebleg * (elave_olunacaq_ay-1)
                son_aya_elave_edilecek_mebleg = cixilacaq_mebleg - a
                inc_month = pd.date_range(odenmeyen_odemetarixler[len(
                    odenmeyen_odemetarixler)-1].tarix, periods=create_olunacaq_ay+1, freq='M')

                muqavile.kredit_muddeti = muqavile.kredit_muddeti + create_olunacaq_ay
                muqavile.save()
                # Var olan aylarin qiymetini musterinin istediyi qiymet edir
                i = 0
                while(i < len(odenmeyen_odemetarixler)):
                    odenmeyen_odemetarixler[i].qiymet = odemek_istediyi_mebleg
                    odenmeyen_odemetarixler[i].save()
                    i += 1
                # Elave olunacaq aylari create edir
                o_t = OdemeTarix.objects.filter(muqavile=muqavile)
                c = int(list(o_t)[-1].ay_no) + 1
                j = 1
                while(j <= create_olunacaq_ay):
                    if(j == create_olunacaq_ay):
                        if(datetime.date.today().day < 29):
                            OdemeTarix.objects.create(
                                ay_no=c,
                                muqavile=muqavile,
                                tarix=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                qiymet=son_aya_elave_edilecek_mebleg,
                                sonuncu_ay=True
                            ).save()
                        elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                            if(inc_month[j].day <= datetime.date.today().day):
                                OdemeTarix.objects.create(
                                    ay_no=c,
                                    muqavile=muqavile,
                                    tarix=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}",
                                    qiymet=son_aya_elave_edilecek_mebleg,
                                    sonuncu_ay=True
                                ).save()
                            else:
                                OdemeTarix.objects.create(
                                    ay_no=c,
                                    muqavile=muqavile,
                                    tarix=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                    qiymet=son_aya_elave_edilecek_mebleg,
                                    sonuncu_ay=True
                                ).save()
                    else:
                        if(datetime.date.today().day < 29):
                            OdemeTarix.objects.create(
                                ay_no=c,
                                muqavile=muqavile,
                                tarix=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                qiymet=odemek_istediyi_mebleg
                            ).save()
                        elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                            if(inc_month[j].day <= datetime.date.today().day):
                                OdemeTarix.objects.create(
                                    ay_no=c,
                                    muqavile=muqavile,
                                    tarix=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}",
                                    qiymet=odemek_istediyi_mebleg
                                ).save()
                            else:
                                OdemeTarix.objects.create(
                                    ay_no=c,
                                    muqavile=muqavile,
                                    tarix=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                                    qiymet=odemek_istediyi_mebleg
                                ).save()
                    c+=1
                    j+= 1
                    
                pdf_create_when_muqavile_updated(
                    sender=muqavile, instance=muqavile, created=True)
                return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Məbləğ cari məbləğdən artıq ola bilməz!"}, status=status.HTTP_400_BAD_REQUEST)
        if (muqavile.muqavile_status == "DÜŞƏN" and request.data.get("muqavile_status") == "DAVAM EDƏN"):
            """
            Müqavilə düşən statusundan davam edən statusuna qaytarılarkən bu hissə işə düşür
            """
            muqavile.muqavile_status = "DAVAM EDƏN"
            muqavile.is_sokuntu = False
            muqavile.save()

            try:
                anbar = get_object_or_404(Anbar, ofis=muqavile.ofis)
            except:
                return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                stok = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)
            except:
                return Response({"detail": "Anbarın stokunda məhsul yoxdur"}, status=status.HTTP_400_BAD_REQUEST)

            if (stok.say < int(mehsul_sayi)):
                return Response({"detail": "Stokda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)

            stok_mehsul_ciximi(stok, mehsul_sayi)

            muqavile_tarixi = muqavile.muqavile_tarixi
            year = muqavile_tarixi.year
            month = muqavile_tarixi.month
            tarix = datetime.date(year=year, month=month, day=1)
            odenmeyen_odemetarixler_qs = OdemeTarix.objects.filter(
                muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")
            odenmeyen_odemetarixler = list(odenmeyen_odemetarixler_qs)
            indi = datetime.datetime.today().strftime('%d-%m-%Y')
            inc_month = pd.date_range(indi, periods=len(
                odenmeyen_odemetarixler), freq='M')
            i = 0
            while (i < len(odenmeyen_odemetarixler)):
                if (datetime.date.today().day < 29):
                    odenmeyen_odemetarixler[
                        i].tarix = f"{inc_month[i].year}-{inc_month[i].month}-{datetime.date.today().day}"
                    odenmeyen_odemetarixler[i].save()
                elif (
                        datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                    odenmeyen_odemetarixler[i].tarix = f"{inc_month[i].year}-{inc_month[i].month}-{inc_month[i].day}",
                    odenmeyen_odemetarixler[i].save()
                i += 1

            create_services(muqavile, muqavile, True)

            return Response({"detail": "Müqavilə düşən statusundan davam edən statusuna keçirildi"},
                            status=status.HTTP_200_OK)

        if (muqavile.muqavile_status == "DAVAM EDƏN" and request.data.get("muqavile_status") == "DÜŞƏN"):
            """
            Müqavilə düşən statusuna keçərkən bu hissə işə düşür
            """
            muqavile_tarixi = muqavile.muqavile_tarixi
            year = muqavile_tarixi.year
            month = muqavile_tarixi.month
            tarix = datetime.date(year=year, month=month, day=1)
            kompensasiya_medaxil = request.data.get("kompensasiya_medaxil")
            kompensasiya_mexaric = request.data.get("kompensasiya_mexaric")

            muqavile_group_leader = muqavile.group_leader
            muqavile_menecer1 = muqavile.menecer1

            ofis_kassa = get_object_or_404(OfisKassa, ofis=muqavile.ofis)
            ofis_kassa_balans = ofis_kassa.balans
            if (kompensasiya_medaxil is not None and kompensasiya_mexaric is not None):
                return Response({"detail": "Kompensasiya məxaric və mədaxil eyni anda edilə bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)

            if (kompensasiya_medaxil is not None):
                ilkin_balans = holding_umumi_balans_hesabla()
                ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

                user = request.user
                musteri = muqavile.musteri

                qeyd = f"GroupLeader - {muqavile_group_leader.asa}, müştəri - {musteri.asa}, tarix - {indiki_tarix_date}, müqavilə düşən statusuna keçirildiyi üçün. Kompensasiya məbləği => {kompensasiya_medaxil}"
                k_medaxil(ofis_kassa, float(kompensasiya_medaxil),
                          muqavile_group_leader, qeyd)

                muqavile.muqavile_status = "DÜŞƏN"
                muqavile.kompensasiya_medaxil = request.data.get("kompensasiya_medaxil")
                muqavile.save()
                
                sonraki_balans = holding_umumi_balans_hesabla()
                ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
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
                    miqdar=float(kompensasiya_medaxil)
                )


            elif (kompensasiya_mexaric is not None):
                if (ofis_kassa_balans < float(kompensasiya_mexaric)):
                    return Response({"detail": "Kompensasiya məxaric məbləği Ofisin balansından çox ola bilməz"},
                                    status=status.HTTP_400_BAD_REQUEST)
                ilkin_balans = holding_umumi_balans_hesabla()
                ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

                user = request.user
                musteri = muqavile.musteri

                qeyd = f"GroupLeader - {muqavile_group_leader.asa}, müştəri - {musteri.asa}, tarix - {indiki_tarix_date}, müqavilə düşən statusuna keçirildiyi üçün. Kompensasiya məbləği => {kompensasiya_mexaric}"
                k_mexaric(ofis_kassa, float(kompensasiya_mexaric),
                          muqavile_group_leader, qeyd)

                muqavile.muqavile_status = "DÜŞƏN"
                muqavile.kompensasiya_mexaric = request.data.get("kompensasiya_mexaric")
                muqavile.save()

                sonraki_balans = holding_umumi_balans_hesabla()
                ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
                pul_axini_create(
                    ofis=muqavile.ofis,
                    shirket=muqavile.ofis.shirket,
                    aciqlama=qeyd,
                    ilkin_balans=ilkin_balans,
                    sonraki_balans=sonraki_balans,
                    ofis_ilkin_balans=ofis_ilkin_balans,
                    ofis_sonraki_balans=ofis_sonraki_balans,
                    emeliyyat_eden=user,
                    emeliyyat_uslubu="MƏXARİC",
                    miqdar=float(kompensasiya_mexaric)
                )

            if (kompensasiya_medaxil == "" and kompensasiya_mexaric == ""):
                muqavile.muqavile_status = "DÜŞƏN"
                muqavile.save()

            muqavile_group_leader = muqavile.group_leader
            muqavile_menecer1 = muqavile.menecer1

            try:
                anbar = get_object_or_404(Anbar, ofis=muqavile.ofis)
            except:
                return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

            stok = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)
            stok_mehsul_elave(stok, mehsul_sayi)

            indi = datetime.date.today()
            d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")
            next_m = d + pd.offsets.MonthBegin(1)

            all_servis = Servis.objects.filter(muqavile=muqavile)
            for servis in all_servis:
                all_servis_odeme = ServisOdeme.objects.filter(
                    servis=servis, odendi=False)
                if len(all_servis_odeme) == 1:
                    all_servis_odeme[0].delete()
                else:
                    for servis_odeme in all_servis_odeme:
                        servis_odeme.delete()
                servis.delete()

            # -------------------- Maaslarin geri qaytarilmasi --------------------
            muqavile_odenis_uslubu = muqavile.odenis_uslubu
            group_leader = muqavile.group_leader
            muqavile_kredit_muddeti = muqavile.kredit_muddeti

            try:
                vezife_adi = group_leader.vezife.vezife_adi
            except:
                vezife_adi = None

            if vezife_adi == "VANLEADER":
                if group_leader is not None:
                    group_leader_status = group_leader.isci_status
                    try:
                        group_leader_vezife = group_leader.vezife.vezife_adi
                    except:
                        group_leader_vezife = None
                    if (group_leader_status is not None):
                        group_leader_prim = GroupLeaderPrimNew.objects.get(
                            prim_status=group_leader_status, vezife=group_leader.vezife)
                        group_leader_mg_indiki_ay = MaasGoruntuleme.objects.get(
                            isci=muqavile_group_leader, tarix=f"{indi.year}-{indi.month}-{1}")
                        group_leader_mg_novbeti_ay = MaasGoruntuleme.objects.get(
                            isci=muqavile_group_leader, tarix=next_m)

                        group_leader_mg_indiki_ay.satis_sayi = float(
                            group_leader_mg_indiki_ay.satis_sayi) - float(mehsul_sayi)
                        group_leader_mg_indiki_ay.satis_meblegi = float(
                            group_leader_mg_indiki_ay.satis_meblegi) - (float(muqavile.mehsul.qiymet) * float(muqavile.mehsul_sayi))

                        # group_leader_mg_novbeti_ay.yekun_maas = float(group_leader_mg_novbeti_ay.yekun_maas) - float(group_leader_prim.komandaya_gore_prim)

                        if muqavile_odenis_uslubu == "NƏĞD":
                            group_leader_mg_novbeti_ay.yekun_maas = float(
                                group_leader_mg_novbeti_ay.yekun_maas) - (float(group_leader_prim.negd) * float(muqavile.mehsul_sayi))
                        elif muqavile_odenis_uslubu == "KREDİT":
                            if int(muqavile_kredit_muddeti) >= 0 and int(muqavile_kredit_muddeti) <= 3:
                                group_leader_mg_novbeti_ay.yekun_maas = float(
                                    group_leader_mg_novbeti_ay.yekun_maas) - (float(group_leader_prim.negd) * float(muqavile.mehsul_sayi))
                            elif int(muqavile_kredit_muddeti) >= 4 and int(muqavile_kredit_muddeti) <= 12:
                                group_leader_mg_novbeti_ay.yekun_maas = float(group_leader_mg_novbeti_ay.yekun_maas) - (
                                    float(group_leader_prim.kredit_4_12) * float(muqavile.mehsul_sayi))
                            elif int(muqavile_kredit_muddeti) >= 13 and int(muqavile_kredit_muddeti) <= 18:
                                group_leader_mg_novbeti_ay.yekun_maas = float(group_leader_mg_novbeti_ay.yekun_maas) - (
                                    float(group_leader_prim.kredit_13_18) * float(muqavile.mehsul_sayi))
                            elif int(muqavile_kredit_muddeti) >= 19 and int(muqavile_kredit_muddeti) <= 24:
                                group_leader_mg_novbeti_ay.yekun_maas = float(group_leader_mg_novbeti_ay.yekun_maas) - (
                                    float(group_leader_prim.kredit_19_24) * float(muqavile.mehsul_sayi))

                        group_leader_mg_indiki_ay.save()
                        group_leader_mg_novbeti_ay.save()

                menecer1 = muqavile.menecer1
                if menecer1 is not None:
                    menecer1_status = menecer1.isci_status
                    try:
                        menecer1_vezife = menecer1.vezife.vezife_adi
                    except:
                        menecer1_vezife = None
                    if (menecer1_vezife == "DEALER"):
                        menecer1_prim = Menecer1PrimNew.objects.get(
                            prim_status=menecer1_status, vezife=menecer1.vezife)
                        menecer1_mg_indiki_ay = MaasGoruntuleme.objects.get(
                            isci=muqavile_menecer1, tarix=f"{indi.year}-{indi.month}-{1}")
                        menecer1_mg_novbeti_ay = MaasGoruntuleme.objects.get(
                            isci=muqavile_menecer1, tarix=next_m)

                        menecer1_mg_indiki_ay.satis_sayi = float(
                            menecer1_mg_indiki_ay.satis_sayi) - float(mehsul_sayi)
                        menecer1_mg_indiki_ay.satis_meblegi = float(menecer1_mg_indiki_ay.satis_meblegi) - (
                            float(muqavile.mehsul.qiymet) * float(muqavile.mehsul_sayi))

                        if muqavile_odenis_uslubu == "NƏĞD":
                            menecer1_mg_novbeti_ay.yekun_maas = float(
                                menecer1_mg_novbeti_ay.yekun_maas) - (float(menecer1_prim.negd) * float(muqavile.mehsul_sayi))
                        elif muqavile_odenis_uslubu == "KREDİT":
                            if int(muqavile_kredit_muddeti) >= 0 and int(muqavile_kredit_muddeti) <= 3:
                                menecer1_mg_novbeti_ay.yekun_maas = float(
                                    menecer1_mg_novbeti_ay.yekun_maas) - (float(menecer1_prim.negd) * float(muqavile.mehsul_sayi))
                            elif int(muqavile_kredit_muddeti) >= 4 and int(muqavile_kredit_muddeti) <= 12:
                                menecer1_mg_novbeti_ay.yekun_maas = float(menecer1_mg_novbeti_ay.yekun_maas) - (
                                    float(menecer1_prim.kredit_4_12) * float(muqavile.mehsul_sayi))
                            elif int(muqavile_kredit_muddeti) >= 13 and int(muqavile_kredit_muddeti) <= 18:
                                menecer1_mg_novbeti_ay.yekun_maas = float(menecer1_mg_novbeti_ay.yekun_maas) - (
                                    float(menecer1_prim.kredit_13_18) * float(muqavile.mehsul_sayi))
                            elif int(muqavile_kredit_muddeti) >= 19 and int(muqavile_kredit_muddeti) <= 24:
                                menecer1_mg_novbeti_ay.yekun_maas = float(menecer1_mg_novbeti_ay.yekun_maas) - (
                                    float(menecer1_prim.kredit_19_24) * float(muqavile.mehsul_sayi))

                        menecer1_mg_indiki_ay.save()
                        menecer1_mg_novbeti_ay.save()

                ofis = muqavile.ofis
                if ofis is not None:
                    officeLeaderVezife = Vezifeler.objects.get(
                        vezife_adi="OFFICE LEADER", shirket=muqavile.shirket)
                    officeLeaders = User.objects.filter(
                        ofis=ofis, vezife=officeLeaderVezife)
                    for officeLeader in officeLeaders:
                        officeLeader_status = officeLeader.isci_status
                        ofisleader_prim = OfficeLeaderPrim.objects.get(
                            prim_status=officeLeader_status, vezife=officeLeader.vezife)

                        officeLeader_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(
                            isci=officeLeader, tarix=f"{indi.year}-{indi.month}-{1}")
                        officeLeader_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(
                            isci=officeLeader, tarix=next_m)

                        officeLeader_maas_goruntulenme_bu_ay.satis_sayi = float(
                            officeLeader_maas_goruntulenme_bu_ay.satis_sayi) - float(mehsul_sayi)
                        officeLeader_maas_goruntulenme_bu_ay.satis_meblegi = float(officeLeader_maas_goruntulenme_bu_ay.satis_meblegi) - (float(muqavile.mehsul.qiymet) * float(muqavile.mehsul_sayi))
                        officeLeader_maas_goruntulenme_bu_ay.save()

                        officeLeader_maas_goruntulenme_novbeti_ay.yekun_maas = float(
                            officeLeader_maas_goruntulenme_novbeti_ay.yekun_maas) - (float(ofisleader_prim.ofise_gore_prim) * float(muqavile.mehsul_sayi))
                        officeLeader_maas_goruntulenme_novbeti_ay.save()
            
            # -------------------- -------------------- --------------------
            muqavile.dusme_tarixi = datetime.date.today()
            muqavile.muqavile_status = "DÜŞƏN"
            muqavile.is_sokuntu = True
            muqavile.save()
            
            return Response({"detail": "Müqavilə düşən statusuna keçirildi"}, status=status.HTTP_200_OK)

        if (muqavile.odenis_uslubu == "KREDİT"):
            if (odemek_istediyi_ilkin_odenis != None and ilkin_odenis_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_ilkin_odenis) != ilkin_odenis):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
                elif (float(odemek_istediyi_ilkin_odenis) == ilkin_odenis):
                    muqavile.ilkin_odenis_status = "BİTMİŞ"
                    muqavile.ilkin_odenis_tarixi = indiki_tarix_date
                    muqavile.qaliq_borc = float(
                        muqavile.qaliq_borc) - float(ilkin_odenis)
                    muqavile.save()
                    return Response({"detail": "İlkin ödəniş ödənildi"}, status=status.HTTP_200_OK)

            if (odemek_istediyi_qaliq_ilkin_odenis != None and ilkin_odenis_status == "BİTMİŞ" and qaliq_ilkin_odenis_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_qaliq_ilkin_odenis) == ilkin_odenis_qaliq):
                    muqavile.qaliq_ilkin_odenis_status = "BİTMİŞ"
                    muqavile.ilkin_odenis_qaliq_tarixi = indiki_tarix_date
                    muqavile.qaliq_borc = float(
                        muqavile.qaliq_borc) - float(ilkin_odenis_qaliq)
                    muqavile.save()
                    return Response({"detail": "Qalıq ilkin ödəniş ödənildi"}, status=status.HTTP_200_OK)
                elif (float(odemek_istediyi_qaliq_ilkin_odenis) != ilkin_odenis_qaliq):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "Bu əməliyyatı icra etmək mümkün olmadı"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception:
        traceback.print_exc()
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)
