import math
from rest_framework import status
from rest_framework.response import Response
from account.models import User, Musteri
from restAPI.v1.contract.serializers import MuqavileSerializer
from company.models import Ofis, Shobe, Vezifeler
from cashbox.models import OfisKassa
from income_expense.models import OfisKassaMedaxil, OfisKassaMexaric
from salary.models import (
    DealerPrim, 
    DealerPrimNew, 
    MaasGoruntuleme, 
    OfficeLeaderPrim, 
    VanLeaderPrim, 
    VanLeaderPrimNew
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


def create_and_add_pdf_when_muqavile_updated(sender, instance, created, **kwargs):
    if created:
        print("create_and_add_pdf_when_muqavile_updated  işə düşdü")

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
        print("create_and_add_pdf_when_muqavile_kredit_updated işə düşdü")

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


def k_mexaric(company_kassa, daxil_edilecek_mebleg, vanleader, qeyd):
    yekun_balans = float(company_kassa.balans) - float(daxil_edilecek_mebleg)
    company_kassa.balans = yekun_balans
    company_kassa.save()
    tarix = datetime.date.today()

    mexaric = OfisKassaMexaric.objects.create(
        mexaric_eden=vanleader,
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

        indi = datetime.datetime.today().strftime('%Y-%m-%d')
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

    vanleader_id = request.data.get("vanleader_id")

    if (vanleader_id == None):
        user = self.request.user
    else:
        user = get_object_or_404(User, pk=vanleader_id)

    dealer_id = request.data.get("dealer_id")
    canvesser_id = request.data.get("canvesser_id")

    musteri_id = request.data.get("musteri_id")
    if musteri_id == None:
        return Response({"detail": "Müştəri qeyd olunmayıb"}, status=status.HTTP_400_BAD_REQUEST)
    musteri = get_object_or_404(Musteri, pk=musteri_id)

    dealer = None
    canvesser = None

    if (dealer_id is not None):
        try:
            dealer = get_object_or_404(User, pk=dealer_id)
            if (canvesser_id == None):
                canvesser = dealer
        except:
            return Response({"detail": "Dealer tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    if (canvesser_id is not None):
        try:
            canvesser = get_object_or_404(User, pk=canvesser_id)
            if (dealer_id == None):
                dealer = canvesser
        except:
            return Response({"detail": "Canvesser tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

    my_time = datetime.datetime.min.time()

    indiki_tarix_date = datetime.date.today()
    indiki_tarix = datetime.datetime.combine(indiki_tarix_date, my_time)
    indiki_tarix_san = datetime.datetime.timestamp(indiki_tarix)

    if (request.data.get("ilkin_odenis_tarixi") is not None):
        ilkin_odenis_tarixi = request.data.get("ilkin_odenis_tarixi")
        ilkin_odenis_tarixi_date = datetime.datetime.strptime(
            ilkin_odenis_tarixi, "%Y-%m-%d")
        ilkin_odenis_tarixi_san = datetime.datetime.timestamp(
            ilkin_odenis_tarixi_date)
    # else:
    #     ilkin_odenis_tarixi = indiki_tarix_date
    #     ilkin_odenis_tarixi_date = indiki_tarix
    #     ilkin_odenis_tarixi_san = indiki_tarix_san

    if (request.data.get("muqavile_tarixi") is not None):
        muqavile_tarixi = request.data.get("muqavile_tarixi")
    else:
        muqavile_tarixi = datetime.date.today()

    if (request.data.get("ilkin_odenis_qaliq_tarixi") is not None):
        ilkin_odenis_qaliq_tarixi = request.data.get(
            "ilkin_odenis_qaliq_tarixi")
        ilkin_odenis_qaliq_tarixi_date = datetime.datetime.strptime(
            ilkin_odenis_qaliq_tarixi, "%Y-%m-%d")
        ilkin_odenis_qaliq_tarixi_san = datetime.datetime.timestamp(
            ilkin_odenis_qaliq_tarixi_date)

    if (request.data.get("negd_odenis_1_tarix") is not None):
        negd_odenis_1_tarix = request.data.get("negd_odenis_1_tarix")
        negd_odenis_1_tarix_date = datetime.datetime.strptime(
            negd_odenis_1_tarix, "%Y-%m-%d")
        negd_odenis_1_tarix_san = datetime.datetime.timestamp(
            negd_odenis_1_tarix_date)

    if (request.data.get("negd_odenis_2_tarix") is not None):
        negd_odenis_2_tarix = request.data.get("negd_odenis_2_tarix")
        negd_odenis_2_tarix_date = datetime.datetime.strptime(
            negd_odenis_2_tarix, "%Y-%m-%d")
        negd_odenis_2_tarix_san = datetime.datetime.timestamp(
            negd_odenis_2_tarix_date)

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

    shobe_id = request.data.get("shobe_id")

    kredit_muddeti = request.data.get("kredit_muddeti")

    if (user.ofis == None):
        ofis = Ofis.objects.get(pk=ofis_id)
    else:
        ofis = user.ofis
    if (user.shirket == None):
        shirket = mehsul.shirket
    else:
        shirket = user.shirket

    if (shobe_id is not None):
        shobe = Shobe.objects.get(pk=shobe_id)
    else:
        shobe = user.shobe
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
                        # return Response(
                        #     {"detail": "İlkin ödəniş məbləği qeyd olunub amma ilkin ödəniş tarixi qeyd olunmayıb"},
                        #     status=status.HTTP_400_BAD_REQUEST)
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

                        serializer.save(vanleader=user, dealer=dealer, canvesser=canvesser, shirket=shirket, ofis=ofis,
                                        shobe=shobe, muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc, muqavile_tarixi=muqavile_tarixi)
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
                            print(f"*****************{ilkin_odenis_tarixi=}")
                            stok_mehsul_ciximi(stok, int(mehsul_sayi))
                            muqavile_umumi_mebleg = umumi_mebleg(mehsul.qiymet, int(mehsul_sayi))
                            
                            ilkin_balans = holding_umumi_balans_hesabla()
                            print(f"{ilkin_balans=}")
                            ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)
                            qeyd = f"Vanleader - {user.asa}, müştəri - {musteri.asa}, tarix - {ilkin_odenis_tarixi}, ödəniş üslubu - {odenis_uslubu}, tam ilkin ödəniş"
                            k_medaxil(ofis_kassa, float(
                                ilkin_odenis), user, qeyd)

                            qaliq_borc = float(
                                muqavile_umumi_mebleg) - float(ilkin_odenis)
                            serializer.save(vanleader=user, dealer=dealer, canvesser=canvesser, shirket=shirket,
                                            ofis=ofis, shobe=shobe, ilkin_odenis=ilkin_odenis,
                                            ilkin_odenis_status="BİTMİŞ", ilkin_odenis_tarixi=ilkin_odenis_tarixi, muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc,)
                            sonraki_balans = holding_umumi_balans_hesabla()
                            print(f"{sonraki_balans=}")
                            ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
                            pul_axini_create(
                                ofis=ofis,
                                shirket=ofis.shirket,
                                aciqlama=f"Vanleader - {user.asa}, müştəri - {musteri.asa}, tarix - {ilkin_odenis_tarixi}, ödəniş üslubu - {odenis_uslubu}, tam ilkin ödəniş",
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

                            serializer.save(vanleader=user, dealer=dealer, canvesser=canvesser, shirket=shirket,
                                            ofis=ofis, shobe=shobe, ilkin_odenis=ilkin_odenis,
                                            ilkin_odenis_status="DAVAM EDƏN", qaliq_borc=qaliq_borc,
                                            muqavile_umumi_mebleg=muqavile_umumi_mebleg, muqavile_tarixi=muqavile_tarixi)
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
                            print(f"{ilkin_balans=}")
                            ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

                            qeyd = f"Vanleader - {user.asa}, müştəri - {musteri.asa}, tarix - {ilkin_odenis_tarixi}, ödəniş üslubu - {odenis_uslubu}, 2-dəfəyə ilkin ödənişin birincisi."
                            k_medaxil(ofis_kassa, float(
                                ilkin_odenis), user, qeyd)

                            qaliq_borc = float(muqavile_umumi_mebleg) - float(ilkin_odenis)

                            serializer.save(vanleader=user, dealer=dealer, canvesser=canvesser, shirket=shirket,
                                            ofis=ofis, shobe=shobe, ilkin_odenis=ilkin_odenis,
                                            ilkin_odenis_qaliq=ilkin_odenis_qaliq, ilkin_odenis_status="BİTMİŞ",
                                            qaliq_ilkin_odenis_status="DAVAM EDƏN",
                                            muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc, muqavile_tarixi=muqavile_tarixi)
                            sonraki_balans = holding_umumi_balans_hesabla()
                            print(f"{sonraki_balans=}")
                            ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
                            pul_axini_create(
                                ofis=ofis,
                                shirket=ofis.shirket,
                                aciqlama=f"Vanleader - {user.asa}, müştəri - {musteri.asa}, tarix - {ilkin_odenis_tarixi}, ödəniş üslubu - {odenis_uslubu}, 2-dəfəyə ilkin ödənişin birincisi.",
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

                            serializer.save(vanleader=user, dealer=dealer, canvesser=canvesser, shirket=shirket,
                                            ofis=ofis, shobe=shobe, ilkin_odenis=ilkin_odenis,
                                            ilkin_odenis_qaliq=ilkin_odenis_qaliq, ilkin_odenis_status="DAVAM EDƏN",
                                            qaliq_ilkin_odenis_status="DAVAM EDƏN",
                                            muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc, muqavile_tarixi=muqavile_tarixi)
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

                            serializer.save(vanleader=user, dealer=dealer, canvesser=canvesser, shirket=shirket,
                                            ofis=ofis, shobe=shobe, ilkin_odenis=ilkin_odenis,
                                            ilkin_odenis_qaliq=ilkin_odenis_qaliq, ilkin_odenis_status="DAVAM EDƏN",
                                            qaliq_ilkin_odenis_status="DAVAM EDƏN",
                                            muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc, muqavile_tarixi=muqavile_tarixi)
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
            elif (odenis_uslubu == "NƏĞD" and request.data.get("negd_odenis_1") == None and request.data.get("negd_odenis_2") == None):
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
                print(f"{ilkin_balans=}")
                ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

                qeyd = f"Vanleader - {user.asa}, müştəri - {musteri.asa}, tarix - {indiki_tarix_date}, ödəniş üslubu - {odenis_uslubu}"
                k_medaxil(ofis_kassa, float(muqavile_umumi_mebleg), user, qeyd)

                serializer.save(vanleader=user, dealer=dealer, canvesser=canvesser, shirket=shirket, ofis=ofis,
                                muqavile_status="BİTMİŞ", shobe=shobe, muqavile_umumi_mebleg=muqavile_umumi_mebleg, muqavile_tarixi=muqavile_tarixi)

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
                    miqdar=float(muqavile_umumi_mebleg)
                )
                # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"}, status=status.HTTP_201_CREATED)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)

            # 2 defeye negd odenis
            elif (request.data.get("negd_odenis_1") is not None and request.data.get("negd_odenis_2") is not None):
                if (float(request.data.get("negd_odenis_1")) < muqavile_umumi_mebleg):
                    if (mehsul_sayi == None):
                        mehsul_sayi = 1
                    if (kredit_muddeti is not None):
                        return Response({"detail": "Kredit müddəti ancaq status kredit olan müqavilələr üçündür"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    negd_odenis_1 = request.data.get("negd_odenis_1")
                    negd_odenis_2 = request.data.get("negd_odenis_2")
                    muqavile_umumi_mebleg = umumi_mebleg(
                        mehsul.qiymet, int(mehsul_sayi))

                    if (negd_odenis_1 == None or negd_odenis_2 == None or negd_odenis_1 == "0" or negd_odenis_2 == "0"):
                        return Response(
                            {"detail": "2 dəfəyə nəğd ödəniş statusunda hər 2 nəğd ödəniş qeyd olunmalıdır"},
                            status=status.HTTP_400_BAD_REQUEST)
                    elif float(negd_odenis_1) > muqavile_umumi_mebleg or float(negd_odenis_2) > muqavile_umumi_mebleg:
                        return Response({"detail": "Daxil etdiyiniz məbləğ müqavilənin ümumi məbləğindən daha çoxdur"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    elif float(negd_odenis_1) + float(negd_odenis_2) == muqavile_umumi_mebleg:
                        if ((indiki_tarix_san == negd_odenis_1_tarix_san) and (
                                indiki_tarix_san < negd_odenis_2_tarix_san)):
                            stok_mehsul_ciximi(stok, int(mehsul_sayi))

                            ilkin_balans = holding_umumi_balans_hesabla()
                            print(f"{ilkin_balans=}")
                            ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

                            qeyd = f"Vanleader - {user.asa}, müştəri - {musteri.asa}, tarix - {negd_odenis_1_tarix}, ödəniş üslubu - {odenis_uslubu}, 1-ci nəğd ödəniş"
                            k_medaxil(ofis_kassa, float(
                                negd_odenis_1), user, qeyd)

                            qaliq_borc = float(
                                muqavile_umumi_mebleg) - float(negd_odenis_1)

                            serializer.save(vanleader=user, dealer=dealer, canvesser=canvesser, shirket=shirket,
                                            ofis=ofis, shobe=shobe, odenis_uslubu="İKİ DƏFƏYƏ NƏĞD",
                                            negd_odenis_1_status="BİTMİŞ", negd_odenis_2_status="DAVAM EDƏN",
                                            muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc, muqavile_tarixi=muqavile_tarixi)
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
                                miqdar=float(negd_odenis_1)
                            )
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

                        elif ((indiki_tarix_san == negd_odenis_1_tarix_san) and (
                                negd_odenis_1_tarix_san == negd_odenis_2_tarix_san)):
                            return Response({"detail": "Ödənişlərin hər ikisi bu günki tarixə qeyd oluna bilməz"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        elif (indiki_tarix_san == negd_odenis_2_tarix_san):
                            return Response({"detail": "Qalıq nəğd ödəniş bu günki tarixə qeyd oluna bilməz"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        elif (negd_odenis_1_tarix_san > negd_odenis_2_tarix_san):
                            return Response(
                                {"detail": "Qalıq nəğd ödəniş tarixi nəğd ödəniş tarixindən əvvəl ola bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)

                        elif (negd_odenis_1_tarix_san == negd_odenis_2_tarix_san):
                            return Response(
                                {"detail": "Qalıq nəğd ödəniş və nəğd ödəniş hər ikisi eyni tarixə qeyd oluna bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)

                        elif ((indiki_tarix_san > negd_odenis_1_tarix_san) or (
                                indiki_tarix_san > negd_odenis_2_tarix_san)):
                            return Response({"detail": "Nəğd ödəniş tarixini keçmiş tarixə təyin edə bilməzsiniz"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        elif ((indiki_tarix_san < negd_odenis_1_tarix_san) and (
                                indiki_tarix_san < negd_odenis_2_tarix_san)):
                            stok_mehsul_ciximi(stok, int(mehsul_sayi))

                            qaliq_borc = float(muqavile_umumi_mebleg)

                            serializer.save(vanleader=user, dealer=dealer, canvesser=canvesser, shirket=shirket,
                                            ofis=ofis, shobe=shobe, odenis_uslubu="İKİ DƏFƏYƏ NƏĞD",
                                            negd_odenis_1_status="DAVAM EDƏN", negd_odenis_2_status="DAVAM EDƏN",
                                            muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc, muqavile_tarixi=muqavile_tarixi)
                            # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                            #                 status=status.HTTP_201_CREATED)
                            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

                    elif (float(negd_odenis_1) + float(negd_odenis_2) != muqavile_umumi_mebleg):
                        return Response({"detail": "Ödəmək istədiyiniz məbləğlər məhsulun qiymətinə bərabər deyil"},
                                        status=status.HTTP_400_BAD_REQUEST)

            elif (request.data.get("negd_odenis_1") is not None and request.data.get("negd_odenis_2") == None):
                return Response({"detail": "Nəğd ödəniş 2 daxil edilməyib"}, status=status.HTTP_400_BAD_REQUEST)

            elif (odenis_uslubu == "İKİ DƏFƏYƏ NƏĞD"):
                if (mehsul_sayi == None):
                    mehsul_sayi = 1
                if (kredit_muddeti is not None):
                    return Response({"detail": "Kredit müddəti ancaq status kredit olan müqavilələr üçündür"},
                                    status=status.HTTP_400_BAD_REQUEST)

                negd_odenis_1 = request.data.get("negd_odenis_1")
                negd_odenis_2 = request.data.get("negd_odenis_2")
                muqavile_umumi_mebleg = umumi_mebleg(
                    mehsul.qiymet, int(mehsul_sayi))

                if (negd_odenis_1 == None or negd_odenis_2 == None or negd_odenis_1 == "0" or negd_odenis_2 == "0"):
                    return Response({"detail": "2 dəfəyə nəğd ödəniş statusunda hər 2 nəğd ödəniş qeyd olunmalıdır"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif (float(negd_odenis_1) > muqavile_umumi_mebleg):
                    return Response({"detail": "Daxil etdiyiniz məbləğ müqavilənin ümumi məbləğindən daha çoxdur"},
                                    status=status.HTTP_400_BAD_REQUEST)

                elif (float(negd_odenis_2) > muqavile_umumi_mebleg):
                    return Response({"detail": "Daxil etdiyiniz məbləğ müqavilənin ümumi məbləğindən daha çoxdur"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif (float(negd_odenis_1) + float(negd_odenis_2) == muqavile_umumi_mebleg):

                    if ((indiki_tarix_san == negd_odenis_1_tarix_san) and (indiki_tarix_san < negd_odenis_2_tarix_san)):
                        stok_mehsul_ciximi(stok, int(mehsul_sayi))
                        
                        ilkin_balans = holding_umumi_balans_hesabla()
                        print(f"{ilkin_balans=}")
                        ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

                        qeyd = f"Vanleader - {user.asa}, müştəri - {musteri.asa}, tarix - {negd_odenis_1_tarix}, ödəniş üslubu - {odenis_uslubu}, 1-ci nəğd ödəniş"
                        k_medaxil(ofis_kassa, float(negd_odenis_1), user, qeyd)

                        qaliq_borc = float(
                            muqavile_umumi_mebleg) - float(negd_odenis_1)

                        serializer.save(vanleader=user, dealer=dealer, canvesser=canvesser, shirket=shirket, ofis=ofis,
                                        shobe=shobe, negd_odenis_1_status="BİTMİŞ", negd_odenis_2_status="DAVAM EDƏN",
                                        muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc, muqavile_tarixi=muqavile_tarixi)
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
                            miqdar=float(negd_odenis_1)
                        )
                        # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                        #                 status=status.HTTP_201_CREATED)
                        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

                    elif ((indiki_tarix_san == negd_odenis_1_tarix_san) and (
                            negd_odenis_1_tarix_san == negd_odenis_2_tarix_san)):
                        return Response({"detail": "Ödənişlərin hər ikisi bu günki tarixə qeyd oluna bilməz"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    elif (indiki_tarix_san == negd_odenis_2_tarix_san):
                        return Response({"detail": "Qalıq nəğd ödəniş bu günki tarixə qeyd oluna bilməz"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    elif (negd_odenis_1_tarix_san > negd_odenis_2_tarix_san):
                        return Response({"detail": "Qalıq nəğd ödəniş tarixi nəğd ödəniş tarixindən əvvəl ola bilməz"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    elif (negd_odenis_1_tarix_san == negd_odenis_2_tarix_san):
                        return Response(
                            {"detail": "Qalıq nəğd ödəniş və nəğd ödəniş hər ikisi eyni tarixə qeyd oluna bilməz"},
                            status=status.HTTP_400_BAD_REQUEST)

                    elif ((indiki_tarix_san > negd_odenis_1_tarix_san) or (indiki_tarix_san > negd_odenis_2_tarix_san)):
                        return Response({"detail": "Nəğd ödəniş tarixini keçmiş tarixə təyin edə bilməzsiniz"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    elif ((indiki_tarix_san < negd_odenis_1_tarix_san) and (
                            indiki_tarix_san < negd_odenis_2_tarix_san)):
                        stok_mehsul_ciximi(stok, int(mehsul_sayi))

                        qaliq_borc = float(muqavile_umumi_mebleg)

                        serializer.save(vanleader=user, dealer=dealer, canvesser=canvesser, shirket=shirket, ofis=ofis,
                                        shobe=shobe, negd_odenis_1_status="DAVAM EDƏN",
                                        negd_odenis_2_status="DAVAM EDƏN", muqavile_umumi_mebleg=muqavile_umumi_mebleg, qaliq_borc=qaliq_borc, muqavile_tarixi=muqavile_tarixi)
                        # return Response({"detail": "Müqavilə müvəffəqiyyətlə imzalandı"},
                        #                 status=status.HTTP_201_CREATED)
                        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

                elif (float(negd_odenis_1) + float(negd_odenis_2) != muqavile_umumi_mebleg):
                    return Response({"detail": "Ödəmək istədiyiniz məbləğlər məhsulun qiymətinə bərabər deyil"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        traceback.print_exc()
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)


def muqavile_patch(self, request, *args, **kwargs):
    """
    DEPRECATED  --- Bu method yenilenmelidir. Istifadesi meslehet gorunmur.
    """
    try:
        muqavile = self.get_object()
        serializer = MuqavileSerializer(
            muqavile, data=request.data, partial=True)

        ilkin_odenis = muqavile.ilkin_odenis
        ilkin_odenis_qaliq = muqavile.ilkin_odenis_qaliq
        ilkin_odenis_status = muqavile.ilkin_odenis_status
        qaliq_ilkin_odenis_status = muqavile.qaliq_ilkin_odenis_status
        odemek_istediyi_ilkin_odenis = request.data.get("ilkin_odenis")
        odemek_istediyi_qaliq_ilkin_odenis = request.data.get(
            "ilkin_odenis_qaliq")

        negd_odenis_1 = muqavile.negd_odenis_1
        negd_odenis_2 = muqavile.negd_odenis_2
        negd_odenis_1_status = muqavile.negd_odenis_1_status
        negd_odenis_2_status = muqavile.negd_odenis_2_status
        muqavile_status = muqavile.muqavile_status
        odemek_istediyi_negd_odenis_1 = request.data.get("negd_odenis_1")
        odemek_istediyi_negd_odenis_2 = request.data.get("negd_odenis_2")
        my_time = datetime.datetime.min.time()

        indiki_tarix_date = datetime.date.today()
        indiki_tarix = datetime.datetime.combine(indiki_tarix_date, my_time)
        indiki_tarix_san = datetime.datetime.timestamp(indiki_tarix)
        dusen_muqavile_status = request.data.get("muqavile_status")
        mehsul = muqavile.mehsul
        mehsul_sayi = muqavile.mehsul_sayi
        muqavile_vanleader = muqavile.vanleader
        musteri_id = request.data.get("musteri_id")
        if (musteri_id is not None):
            musteri = get_object_or_404(Musteri, pk=musteri_id)

        muqavile_dealer = muqavile.dealer
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
                muqavile=muqavile, odenme_status="ÖDƏNMƏYƏN")

            odemek_istediyi_mebleg = float(
                request.data.get("yeni_qrafik_mebleg"))

            odenen_mebleg = 0
            for i in odenen_odemetarixler:
                odenen_mebleg += float(i.qiymet)

            odediyi = float(odenen_mebleg) + ilkin_odenis_tam
            qaliq_borc = mehsulun_qiymeti - odediyi
            odenmeyen_aylar = len(odenmeyen_odemetarixler)

            try:
                elave_olunacaq_ay_qaliqli = qaliq_borc / odemek_istediyi_mebleg
                # muqavile.yeni_qrafik_status = "YENİ QRAFİK"
                muqavile.save()
            except:
                return Response({"detail": "Ödəmək istədiyiniz məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

            elave_olunacaq_ay = math.ceil(elave_olunacaq_ay_qaliqli)
            create_olunacaq_ay = elave_olunacaq_ay - \
                len(odenmeyen_odemetarixler)
            a = odemek_istediyi_mebleg * (elave_olunacaq_ay-1)
            son_aya_elave_edilecek_mebleg = qaliq_borc - a
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
            j = 1
            while(j <= create_olunacaq_ay):
                if(j == create_olunacaq_ay):
                    if(datetime.date.today().day < 29):
                        OdemeTarix.objects.create(
                            muqavile=muqavile,
                            tarix=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                            qiymet=son_aya_elave_edilecek_mebleg
                        )
                    elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                        if(inc_month[j].day <= datetime.date.today().day):
                            OdemeTarix.objects.create(
                                muqavile=muqavile,
                                tarix=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}",
                                qiymet=son_aya_elave_edilecek_mebleg
                            )
                else:
                    if(datetime.date.today().day < 29):
                        OdemeTarix.objects.create(
                            muqavile=muqavile,
                            tarix=f"{inc_month[j].year}-{inc_month[j].month}-{datetime.date.today().day}",
                            qiymet=odemek_istediyi_mebleg
                        )
                    elif(datetime.date.today().day == 31 or datetime.date.today().day == 30 or datetime.date.today().day == 29):
                        if(inc_month[j].day <= datetime.date.today().day):
                            OdemeTarix.objects.create(
                                muqavile=muqavile,
                                tarix=f"{inc_month[j].year}-{inc_month[j].month}-{inc_month[j].day}",
                                qiymet=odemek_istediyi_mebleg
                            )
                j += 1
            return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)

        if (muqavile.muqavile_status == "DÜŞƏN" and request.data.get("muqavile_status") == "DAVAM EDƏN"):
            """
            Müqavilə düşən statusundan davam edən statusuna qaytarılarkən bu hissə işə düşür
            """
            muqavile.muqavile_status = "DAVAM EDƏN"
            muqavile.save()

            try:
                anbar = get_object_or_404(Anbar, ofis=muqavile_vanleader.ofis)
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
            indi = datetime.datetime.today().strftime('%Y-%m-%d')
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

            muqavile_vanleader = muqavile.vanleader
            muqavile_dealer = muqavile.dealer

            ofis_kassa = get_object_or_404(OfisKassa, ofis=muqavile.ofis)
            ofis_kassa_balans = ofis_kassa.balans

            if (kompensasiya_medaxil is not None and kompensasiya_mexaric is not None):
                return Response({"detail": "Kompensasiya məxaric və mədaxil eyni anda edilə bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)

            if (kompensasiya_medaxil is not None):
                ilkin_balans = holding_umumi_balans_hesabla()
                print(f"{ilkin_balans=}")
                ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

                qeyd = f"Vanleader - {muqavile_vanleader.asa}, müştəri - {musteri.asa}, tarix - {indiki_tarix_date}, müqavilə düşən statusuna keçirildiyi üçün."
                k_medaxil(ofis_kassa, float(kompensasiya_medaxil),
                          muqavile_vanleader, qeyd)
                user = request.user
                muqavile.muqavile_status = "DÜŞƏN"
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
                    miqdar=float(kompensasiya_medaxil)
                )

            elif (kompensasiya_mexaric is not None):
                if (ofis_kassa_balans < float(kompensasiya_mexaric)):
                    return Response({"detail": "Kompensasiya məxaric məbləği Ofisin balansından çox ola bilməz"},
                                    status=status.HTTP_400_BAD_REQUEST)
                ilkin_balans = holding_umumi_balans_hesabla()
                print(f"{ilkin_balans=}")
                ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

                qeyd = f"Vanleader - {muqavile_vanleader.asa}, müştəri - {musteri.asa}, tarix - {indiki_tarix_date}, müqavilə düşən statusuna keçirildiyi üçün. Kompensasiya məbləği=> {kompensasiya_mexaric} AZN."
                k_mexaric(ofis_kassa, float(kompensasiya_mexaric),
                          muqavile_vanleader, qeyd)

                muqavile.muqavile_status = "DÜŞƏN"
                muqavile.save()

                sonraki_balans = holding_umumi_balans_hesabla()
                print(f"{sonraki_balans=}")
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

            muqavile_vanleader = muqavile.vanleader
            muqavile_dealer = muqavile.dealer

            try:
                anbar = get_object_or_404(Anbar, ofis=muqavile.ofis)
            except:
                return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

            stok = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)
            stok_mehsul_elave(stok, mehsul_sayi)
            indi = datetime.date.today()
            d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")
            next_m = d + pd.offsets.MonthBegin(1)
            all_servis = Servis.objects.filter(muqavile=self.get_object())

            for servis in all_servis:
                all_servis_odeme = ServisOdeme.objects.filter(
                    servis=servis, odendi=False)
                if len(all_servis_odeme) == 1:
                    servis_odeme = all_servis_odeme[0]
                    servis_odeme.delete()
                    servis.delete()
                for servis_odeme in all_servis_odeme:
                    servis_odeme.delete()

            # -------------------- Maaslarin geri qaytarilmasi --------------------
            muqavile_odenis_uslubu = muqavile.odenis_uslubu
            vanleader = muqavile.vanleader
            if vanleader is not None:
                vanleader_status = vanleader.isci_status
                try:
                    vanleader_vezife_all = vanleader.vezife.all()
                    vanleader_vezife = vanleader_vezife_all[0].vezife_adi
                except:
                    vanleader_vezife = None
                if (vanleader_status is not None):
                    vanleader_prim = VanLeaderPrim.objects.get(
                        prim_status=vanleader_status, odenis_uslubu=muqavile_odenis_uslubu)

                    vanleader_mg_indiki_ay = MaasGoruntuleme.objects.get(
                        isci=muqavile_vanleader, tarix=f"{indi.year}-{indi.month}-{1}")
                    vanleader_mg_novbeti_ay = MaasGoruntuleme.objects.get(
                        isci=muqavile_vanleader, tarix=next_m)

                    vanleader_mg_indiki_ay.satis_sayi = float(
                        vanleader_mg_indiki_ay.satis_sayi) - float(mehsul_sayi)
                    vanleader_mg_indiki_ay.satis_meblegi = float(
                        vanleader_mg_indiki_ay.satis_meblegi) - float(muqavile.mehsul.qiymet)

                    vanleader_mg_novbeti_ay.yekun_maas = float(
                        vanleader_mg_novbeti_ay.yekun_maas) - float(vanleader_prim.komandaya_gore_prim)

                    vanleader_mg_indiki_ay.save()
                    vanleader_mg_novbeti_ay.save()

            dealer = muqavile.dealer
            if dealer is not None:
                dealer_status = dealer.isci_status
                try:
                    dealer_vezife_all = dealer.vezife.all()
                    dealer_vezife = dealer_vezife_all[0].vezife_adi
                except:
                    dealer_vezife = None
                if (dealer_vezife == "DEALER"):
                    dealer_prim = DealerPrim.objects.get(
                        prim_status=dealer_status, odenis_uslubu=muqavile_odenis_uslubu)

                    dealer_mg_indiki_ay = MaasGoruntuleme.objects.get(
                        isci=muqavile_dealer, tarix=f"{indi.year}-{indi.month}-{1}")
                    dealer_mg_novbeti_ay = MaasGoruntuleme.objects.get(
                        isci=muqavile_dealer, tarix=next_m)

                    dealer_mg_indiki_ay.satis_sayi = float(
                        dealer_mg_indiki_ay.satis_sayi) - float(mehsul_sayi)
                    dealer_mg_indiki_ay.satis_meblegi = float(
                        dealer_mg_indiki_ay.satis_meblegi) - float(muqavile.mehsul.qiymet)
                    dealer_mg_novbeti_ay.yekun_maas = float(
                        dealer_mg_novbeti_ay.yekun_maas) - float(dealer_prim.komandaya_gore_prim)

                    dealer_mg_indiki_ay.save()
                    dealer_mg_novbeti_ay.save()

            ofis = muqavile.ofis
            if ofis is not None:
                officeLeaderVezife = Vezifeler.objects.get(
                    vezife_adi="OFFICE LEADER")
                officeLeaders = User.objects.filter(
                    ofis=ofis, vezife=officeLeaderVezife)
                for officeLeader in officeLeaders:
                    officeLeader_status = officeLeader.isci_status
                    ofisleader_prim = OfficeLeaderPrim.objects.get(
                        prim_status=officeLeader_status)

                    officeLeader_maas_goruntulenme_bu_ay = MaasGoruntuleme.objects.get(
                        isci=officeLeader, tarix=f"{indi.year}-{indi.month}-{1}")
                    officeLeader_maas_goruntulenme_novbeti_ay = MaasGoruntuleme.objects.get(
                        isci=officeLeader, tarix=next_m)

                    officeLeader_maas_goruntulenme_bu_ay.satis_sayi = float(
                        officeLeader_maas_goruntulenme_bu_ay.satis_sayi) - float(mehsul_sayi)
                    officeLeader_maas_goruntulenme_bu_ay.satis_meblegi = float(
                        officeLeader_maas_goruntulenme_bu_ay.satis_meblegi) - float(muqavile.mehsul.qiymet)
                    officeLeader_maas_goruntulenme_bu_ay.save()

                    officeLeader_maas_goruntulenme_novbeti_ay.yekun_maas = float(
                        officeLeader_maas_goruntulenme_novbeti_ay.yekun_maas) - float(ofisleader_prim.komandaya_gore_prim)
                    officeLeader_maas_goruntulenme_novbeti_ay.save()
            # -------------------- -------------------- --------------------
            muqavile.muqavile_status = "DÜŞƏN"
            muqavile.save()
            return Response({"detail": "Müqavilə düşən statusuna keçirildi"}, status=status.HTTP_200_OK)

        if (muqavile.odenis_uslubu == "KREDİT"):
            if (odemek_istediyi_ilkin_odenis != None and ilkin_odenis_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_ilkin_odenis) != ilkin_odenis):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
                elif (float(odemek_istediyi_ilkin_odenis) == ilkin_odenis):
                    muqavile.ilkin_odenis_status = "BİTMİŞ"
                    muqavile.ilkin_odenis_tarixi = indiki_tarix_date
                    muqavile.save()
                    return Response({"detail": "İlkin ödəniş ödənildi"}, status=status.HTTP_200_OK)

            if (
                    odemek_istediyi_qaliq_ilkin_odenis != None and ilkin_odenis_status == "BİTMİŞ" and qaliq_ilkin_odenis_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_qaliq_ilkin_odenis) == ilkin_odenis_qaliq):
                    muqavile.qaliq_ilkin_odenis_status = "BİTMİŞ"
                    muqavile.ilkin_odenis_qaliq_tarixi = indiki_tarix_date
                    muqavile.save()
                    return Response({"detail": "Qalıq ilkin ödəniş ödənildi"}, status=status.HTTP_200_OK)
                elif (float(odemek_istediyi_qaliq_ilkin_odenis) != ilkin_odenis_qaliq):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        if (muqavile.odenis_uslubu == "İKİ DƏFƏYƏ NƏĞD"):
            if (odemek_istediyi_negd_odenis_1 != None and negd_odenis_1_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_negd_odenis_1) != negd_odenis_1):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
                elif (float(odemek_istediyi_negd_odenis_1) == negd_odenis_1):
                    muqavile.negd_odenis_1_status = "BİTMİŞ"
                    muqavile.negd_odenis_1_tarix = indiki_tarix_date
                    muqavile.save()
                    return Response({"detail": "1-ci ödəniş ödənildi"}, status=status.HTTP_200_OK)

            if (
                    odemek_istediyi_negd_odenis_2 != None and negd_odenis_1_status == "BİTMİŞ" and negd_odenis_2_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_negd_odenis_2) == negd_odenis_2):
                    muqavile.negd_odenis_2_status = "BİTMİŞ"
                    muqavile.negd_odenis_2_tarix = indiki_tarix_date
                    muqavile.muqavile_status = "BİTMİŞ"
                    muqavile.save()
                    return Response({"detail": "Qalıq nəğd ödəniş ödənildi"}, status=status.HTTP_200_OK)
                elif (float(odemek_istediyi_negd_odenis_2) != negd_odenis_2):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        traceback.print_exc()


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

        negd_odenis_1 = muqavile.negd_odenis_1
        negd_odenis_2 = muqavile.negd_odenis_2
        negd_odenis_1_status = muqavile.negd_odenis_1_status
        negd_odenis_2_status = muqavile.negd_odenis_2_status

        muqavile_status = muqavile.muqavile_status
        odemek_istediyi_negd_odenis_1 = request.data.get("negd_odenis_1")
        odemek_istediyi_negd_odenis_2 = request.data.get("negd_odenis_2")
        my_time = datetime.datetime.min.time()

        indiki_tarix_date = datetime.date.today()
        indiki_tarix = datetime.datetime.combine(indiki_tarix_date, my_time)
        indiki_tarix_san = datetime.datetime.timestamp(indiki_tarix)
        dusen_muqavile_status = request.data.get("muqavile_status")
        mehsul = muqavile.mehsul
        mehsul_sayi = muqavile.mehsul_sayi
        muqavile_vanleader = muqavile.vanleader
        ofis=muqavile.ofis
        musteri = muqavile.musteri
        musteri_id = request.data.get("musteri_id")
        if (musteri_id is not None):
            musteri = get_object_or_404(Musteri, pk=musteri_id)

        muqavile_dealer = muqavile.dealer
        yeni_qrafik = request.data.get("yeni_qrafik_status")
        # YENI QRAFIK ile bagli emeliyyatlar
        if(yeni_qrafik == "YENİ QRAFİK"):
            print("------------------------------------------------------------------------------------")
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
                print(f"***************{sertli_odeme=}")
                print(f"***************{sertli_odemeden_gelen_mebleg=}")
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

                print(f"|||||||||||||||||||{inc_month=}")
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
                print(f"***************{c=}")
                print(f"***************{create_olunacaq_ay=}")
                print(f"***************{datetime.date.today().day=} ---type---> {type(datetime.date.today().day)=}")
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
                            print(f"**************{j=}")
                            print(f"***testson1***********{inc_month[j].day=} ---type---> {type(inc_month[j].day)=}")
                            print(f"***testson1***********{datetime.date.today().day=} ---type---> {type(datetime.date.today().day)=}")
                            print("Burdayam3")
                            if(inc_month[j].day <= datetime.date.today().day):
                                print(f"***testson2***********{inc_month[j].day=} ---type---> {type(inc_month[j].day)=}")
                                print(f"***testson2***********{datetime.date.today().day=} ---type---> {type(datetime.date.today().day)=}")
                                print("Burdayam4")
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
                            print(f"**************{j=}")
                            print(f"***test***********{inc_month[j].day=} ---type---> {type(inc_month[j].day)=}")
                            print(f"***test***********{datetime.date.today().day=} ---type---> {type(datetime.date.today().day)=}")
                            print("Burdayam1")

                            print(f"***test***********{datetime.date.today().day=} ---type---> {type(datetime.date.today().day)=}")
                            if(inc_month[j].day <= datetime.date.today().day):
                                print(f"**************{j=}")
                                print(f"***test***********{inc_month[j].day=} ---type---> {type(inc_month[j].day)=}")
                                print(f"***test***********{datetime.date.today().day=} ---type---> {type(datetime.date.today().day)=}")
                                print("Burdayam2")

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
            indi = datetime.datetime.today().strftime('%Y-%m-%d')
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

            muqavile_vanleader = muqavile.vanleader
            muqavile_dealer = muqavile.dealer

            ofis_kassa = get_object_or_404(OfisKassa, ofis=muqavile.ofis)
            ofis_kassa_balans = ofis_kassa.balans
            if (kompensasiya_medaxil is not None and kompensasiya_mexaric is not None):
                return Response({"detail": "Kompensasiya məxaric və mədaxil eyni anda edilə bilməz"},
                                status=status.HTTP_400_BAD_REQUEST)

            if (kompensasiya_medaxil is not None):
                ilkin_balans = holding_umumi_balans_hesabla()
                print(f"{ilkin_balans=}")
                ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

                user = request.user
                musteri = muqavile.musteri

                qeyd = f"Vanleader - {muqavile_vanleader.asa}, müştəri - {musteri.asa}, tarix - {indiki_tarix_date}, müqavilə düşən statusuna keçirildiyi üçün. Kompensasiya məbləği => {kompensasiya_medaxil}"
                k_medaxil(ofis_kassa, float(kompensasiya_medaxil),
                          muqavile_vanleader, qeyd)

                muqavile.muqavile_status = "DÜŞƏN"
                muqavile.kompensasiya_medaxil = request.data.get("kompensasiya_medaxil")
                muqavile.save()
                
                sonraki_balans = holding_umumi_balans_hesabla()
                print(f"{sonraki_balans=}")
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
                print(f"{ilkin_balans=}")
                ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

                user = request.user
                musteri = muqavile.musteri

                qeyd = f"Vanleader - {muqavile_vanleader.asa}, müştəri - {musteri.asa}, tarix - {indiki_tarix_date}, müqavilə düşən statusuna keçirildiyi üçün. Kompensasiya məbləği => {kompensasiya_mexaric}"
                k_mexaric(ofis_kassa, float(kompensasiya_mexaric),
                          muqavile_vanleader, qeyd)

                muqavile.muqavile_status = "DÜŞƏN"
                muqavile.kompensasiya_mexaric = request.data.get("kompensasiya_mexaric")
                muqavile.save()

                sonraki_balans = holding_umumi_balans_hesabla()
                print(f"{sonraki_balans=}")
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

            muqavile_vanleader = muqavile.vanleader
            muqavile_dealer = muqavile.dealer

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
            print(f"{all_servis=}")
            for servis in all_servis:
                all_servis_odeme = ServisOdeme.objects.filter(
                    servis=servis, odendi=False)
                print(f"{all_servis_odeme=}")
                if len(all_servis_odeme) == 1:
                    all_servis_odeme[0].delete()
                else:
                    for servis_odeme in all_servis_odeme:
                        print(f"{servis_odeme=}")
                        servis_odeme.delete()
                servis.delete()

            # -------------------- Maaslarin geri qaytarilmasi --------------------
            muqavile_odenis_uslubu = muqavile.odenis_uslubu
            vanleader = muqavile.vanleader
            muqavile_kredit_muddeti = muqavile.kredit_muddeti

            try:
                vezife_adi = vanleader.vezife.vezife_adi
            except:
                vezife_adi = None

            if vezife_adi == "VANLEADER":
                if vanleader is not None:
                    vanleader_status = vanleader.isci_status
                    try:
                        vanleader_vezife = vanleader.vezife.vezife_adi
                    except:
                        vanleader_vezife = None
                    if (vanleader_status is not None):
                        vanleader_prim = VanLeaderPrimNew.objects.get(
                            prim_status=vanleader_status, vezife=vanleader.vezife)
                        vanleader_mg_indiki_ay = MaasGoruntuleme.objects.get(
                            isci=muqavile_vanleader, tarix=f"{indi.year}-{indi.month}-{1}")
                        vanleader_mg_novbeti_ay = MaasGoruntuleme.objects.get(
                            isci=muqavile_vanleader, tarix=next_m)

                        vanleader_mg_indiki_ay.satis_sayi = float(
                            vanleader_mg_indiki_ay.satis_sayi) - float(mehsul_sayi)
                        vanleader_mg_indiki_ay.satis_meblegi = float(
                            vanleader_mg_indiki_ay.satis_meblegi) - (float(muqavile.mehsul.qiymet) * float(muqavile.mehsul_sayi))

                        # vanleader_mg_novbeti_ay.yekun_maas = float(vanleader_mg_novbeti_ay.yekun_maas) - float(vanleader_prim.komandaya_gore_prim)

                        if muqavile_odenis_uslubu == "NƏĞD":
                            vanleader_mg_novbeti_ay.yekun_maas = float(
                                vanleader_mg_novbeti_ay.yekun_maas) - (float(vanleader_prim.negd) * float(muqavile.mehsul_sayi))
                        elif muqavile_odenis_uslubu == "KREDİT":
                            if int(muqavile_kredit_muddeti) >= 0 and int(muqavile_kredit_muddeti) <= 3:
                                vanleader_mg_novbeti_ay.yekun_maas = float(
                                    vanleader_mg_novbeti_ay.yekun_maas) - (float(vanleader_prim.negd) * float(muqavile.mehsul_sayi))
                            elif int(muqavile_kredit_muddeti) >= 4 and int(muqavile_kredit_muddeti) <= 12:
                                vanleader_mg_novbeti_ay.yekun_maas = float(vanleader_mg_novbeti_ay.yekun_maas) - (
                                    float(vanleader_prim.kredit_4_12) * float(muqavile.mehsul_sayi))
                            elif int(muqavile_kredit_muddeti) >= 13 and int(muqavile_kredit_muddeti) <= 18:
                                vanleader_mg_novbeti_ay.yekun_maas = float(vanleader_mg_novbeti_ay.yekun_maas) - (
                                    float(vanleader_prim.kredit_13_18) * float(muqavile.mehsul_sayi))
                            elif int(muqavile_kredit_muddeti) >= 19 and int(muqavile_kredit_muddeti) <= 24:
                                vanleader_mg_novbeti_ay.yekun_maas = float(vanleader_mg_novbeti_ay.yekun_maas) - (
                                    float(vanleader_prim.kredit_19_24) * float(muqavile.mehsul_sayi))

                        vanleader_mg_indiki_ay.save()
                        vanleader_mg_novbeti_ay.save()

                dealer = muqavile.dealer
                if dealer is not None:
                    dealer_status = dealer.isci_status
                    try:
                        dealer_vezife = dealer.vezife.vezife_adi
                    except:
                        dealer_vezife = None
                    if (dealer_vezife == "DEALER"):
                        dealer_prim = DealerPrimNew.objects.get(
                            prim_status=dealer_status, vezife=dealer.vezife)
                        dealer_mg_indiki_ay = MaasGoruntuleme.objects.get(
                            isci=muqavile_dealer, tarix=f"{indi.year}-{indi.month}-{1}")
                        dealer_mg_novbeti_ay = MaasGoruntuleme.objects.get(
                            isci=muqavile_dealer, tarix=next_m)

                        dealer_mg_indiki_ay.satis_sayi = float(
                            dealer_mg_indiki_ay.satis_sayi) - float(mehsul_sayi)
                        dealer_mg_indiki_ay.satis_meblegi = float(dealer_mg_indiki_ay.satis_meblegi) - (
                            float(muqavile.mehsul.qiymet) * float(muqavile.mehsul_sayi))

                        if muqavile_odenis_uslubu == "NƏĞD":
                            dealer_mg_novbeti_ay.yekun_maas = float(
                                dealer_mg_novbeti_ay.yekun_maas) - (float(dealer_prim.negd) * float(muqavile.mehsul_sayi))
                        elif muqavile_odenis_uslubu == "KREDİT":
                            if int(muqavile_kredit_muddeti) >= 0 and int(muqavile_kredit_muddeti) <= 3:
                                dealer_mg_novbeti_ay.yekun_maas = float(
                                    dealer_mg_novbeti_ay.yekun_maas) - (float(dealer_prim.negd) * float(muqavile.mehsul_sayi))
                            elif int(muqavile_kredit_muddeti) >= 4 and int(muqavile_kredit_muddeti) <= 12:
                                dealer_mg_novbeti_ay.yekun_maas = float(dealer_mg_novbeti_ay.yekun_maas) - (
                                    float(dealer_prim.kredit_4_12) * float(muqavile.mehsul_sayi))
                            elif int(muqavile_kredit_muddeti) >= 13 and int(muqavile_kredit_muddeti) <= 18:
                                dealer_mg_novbeti_ay.yekun_maas = float(dealer_mg_novbeti_ay.yekun_maas) - (
                                    float(dealer_prim.kredit_13_18) * float(muqavile.mehsul_sayi))
                            elif int(muqavile_kredit_muddeti) >= 19 and int(muqavile_kredit_muddeti) <= 24:
                                dealer_mg_novbeti_ay.yekun_maas = float(dealer_mg_novbeti_ay.yekun_maas) - (
                                    float(dealer_prim.kredit_19_24) * float(muqavile.mehsul_sayi))

                        dealer_mg_indiki_ay.save()
                        dealer_mg_novbeti_ay.save()

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

        if (muqavile.odenis_uslubu == "İKİ DƏFƏYƏ NƏĞD"):
            if (odemek_istediyi_negd_odenis_1 != None and negd_odenis_1_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_negd_odenis_1) != negd_odenis_1):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
                elif (float(odemek_istediyi_negd_odenis_1) == negd_odenis_1):
                    muqavile.negd_odenis_1_status = "BİTMİŞ"
                    muqavile.negd_odenis_1_tarix = indiki_tarix_date
                    muqavile.qaliq_borc = float(
                        muqavile.qaliq_borc) - float(negd_odenis_1)
                    muqavile.save()
                    return Response({"detail": "1-ci ödəniş ödənildi"}, status=status.HTTP_200_OK)

            if (
                    odemek_istediyi_negd_odenis_2 != None and negd_odenis_1_status == "BİTMİŞ" and negd_odenis_2_status == "DAVAM EDƏN"):
                if (float(odemek_istediyi_negd_odenis_2) == negd_odenis_2):
                    muqavile.negd_odenis_2_status = "BİTMİŞ"
                    muqavile.negd_odenis_2_tarix = indiki_tarix_date
                    muqavile.muqavile_status = "BİTMİŞ"
                    muqavile.qaliq_borc = float(
                        muqavile.qaliq_borc) - float(negd_odenis_2)
                    muqavile.save()
                    return Response({"detail": "Qalıq nəğd ödəniş ödənildi"}, status=status.HTTP_200_OK)
                elif (float(odemek_istediyi_negd_odenis_2) != negd_odenis_2):
                    return Response({"detail": "Məbləği düzgün daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

        if muqavile.odenis_uslubu == "İKİ DƏFƏYƏ NƏĞD":
            if serializer.is_valid():
                kredit_muddeti = serializer.validated_data.get(
                    "kredit_muddeti")
                odenis_uslubu = serializer.validated_data.get("odenis_uslubu")

                if odenis_uslubu == "KREDİT":

                    ilkin_odenis = 0
                    ilkin_odenis_qaliq = 0
                    negd_odenis_1 = muqavile.negd_odenis_1
                    negd_odenis_2 = muqavile.negd_odenis_2
                    negd_odenis_1_tarix = muqavile.negd_odenis_1_tarix
                    negd_odenis_2_tarix = muqavile.negd_odenis_2_tarix
                    negd_odenis_1_status = muqavile.negd_odenis_1_status
                    negd_odenis_2_status = muqavile.negd_odenis_2_status

                    if negd_odenis_1_tarix != datetime.date.today():
                        negd_odenis_1_status = "DAVAM EDƏN"
                    else:
                        negd_odenis_1_status = "YOXDUR"

                    if negd_odenis_2_tarix != datetime.date.today():
                        negd_odenis_2_status = "DAVAM EDƏN"
                    else:
                        negd_odenis_2_status = "YOXDUR"

                    create_odeme_tarix_when_update_muqavile(
                        instance=muqavile,
                        kredit_muddeti=int(kredit_muddeti),
                        odenis_uslubu=odenis_uslubu,
                        ilkin_odenis=float(negd_odenis_1),
                        ilkin_odenis_qaliq=0
                    )
                    serializer.save(
                        muqavile_status="DAVAM EDƏN",
                        ilkin_odenis=negd_odenis_1,
                        ilkin_odenis_qaliq=0,
                        ilkin_odenis_tarixi=negd_odenis_1_tarix,
                        ilkin_odenis_qaliq_tarixi=None,
                        ilkin_odenis_status=negd_odenis_1_status,
                        qaliq_ilkin_odenis_status="YOXDUR",
                        negd_odenis_1=0,
                        negd_odenis_2=0,
                        negd_odenis_1_tarix=None,
                        negd_odenis_2_tarix=None,
                        negd_odenis_1_status="YOXDUR",
                        negd_odenis_2_status="YOXDUR"
                    )
                    pdf_create_when_muqavile_updated(
                        sender=muqavile, instance=muqavile, created=True)
                    return Response({"detail": "Müqavilə nəğd statusundan kredit statusuna keçirildi"}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Bu əməliyyatı icra etmək mümkün olmadı"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception:
        traceback.print_exc()
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)
