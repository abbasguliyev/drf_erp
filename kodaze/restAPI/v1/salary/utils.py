import pandas as pd
from company.models import (
    Holding,
)
from cashbox.models import (
    HoldingKassa, 
    OfisKassa, 
    ShirketKassa, 
)
from income_expense.models import (
    HoldingKassaMexaric, 
    OfisKassaMexaric, 
    ShirketKassaMexaric
)
from salary.models import MaasGoruntuleme
from rest_framework import status

from rest_framework.response import Response
import datetime

from restAPI.v1.cashbox.utils import (
    holding_umumi_balans_hesabla, 
    pul_axini_create, 
    ofis_balans_hesabla, 
    shirket_balans_hesabla, 
    holding_balans_hesabla
)
def maas_ode_create(self, request, *args, **kwargs):
    """
    İşçilərə maas vermək funksiyası
    """
    serializer = self.get_serializer(data=request.data)
    user = self.request.user
    # isciler = serializer.data.get("isci")

    if serializer.is_valid():
        isciler = serializer.validated_data.get("isci")
        qeyd = serializer.validated_data.get("qeyd")
        odeme_tarixi = serializer.validated_data.get("odeme_tarixi")
        if (serializer.validated_data.get("odeme_tarixi") == None):
            odeme_tarixi = datetime.date.today()
        if (serializer.validated_data.get("odeme_tarixi") == ""):
            odeme_tarixi = datetime.date.today()

        indi = datetime.date.today()
        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)

        yekun_odenen_mebleg = 0
        for isci in isciler:
            try:
                maas_goruntuleme = MaasGoruntuleme.objects.get(isci=isci, tarix=f"{indi.year}-{indi.month}-{1}")
            except:
                return Response({"detail": f"{isci} işçinin maaş kartında xəta var"}, status=status.HTTP_404_NOT_FOUND)

            mebleg = maas_goruntuleme.yekun_maas
            yekun_odenen_mebleg += float(mebleg)
            maas_goruntuleme.yekun_maas = 0
            ofis = isci.ofis
            shirket = isci.shirket
            holding = Holding.objects.all()[0]

            ilkin_balans = holding_umumi_balans_hesabla()
            print(f"{ilkin_balans=}")
            ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)
            shirket_ilkin_balans = shirket_balans_hesabla(shirket=shirket)
            holding_ilkin_balans = holding_balans_hesabla()

            qeyd = f"{user.asa} tərəfindən {isci.asa} adlı işçiyə {mebleg} AZN maaş ödəndi"

            if ofis is not None:
                ofis_kassa = OfisKassa.objects.get(ofis=ofis)
                if float(ofis_kassa.balans) < float(mebleg):
                    return Response({"detail": "Ofisin kassasında yetəri qədər məbləğ yoxdur"})
                ofis_kassa.balans = float(ofis_kassa.balans) - float(mebleg)
                ofis_kassa.save()
                ofis_kassa_mexaric = OfisKassaMexaric.objects.create(
                    mexaric_eden=user,
                    ofis_kassa=ofis_kassa,
                    mebleg=mebleg,
                    mexaric_tarixi=odeme_tarixi,
                    qeyd=qeyd
                )
                ofis_kassa_mexaric.save()

                sonraki_balans = holding_umumi_balans_hesabla()
                print(f"{sonraki_balans=}")
                ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
                pul_axini_create(
                    ofis=ofis,
                    shirket= ofis.shirket,
                    aciqlama=qeyd,
                    ilkin_balans=ilkin_balans,
                    sonraki_balans=sonraki_balans,
                    ofis_ilkin_balans=ofis_ilkin_balans,
                    ofis_sonraki_balans=ofis_sonraki_balans,
                    emeliyyat_eden=user,
                    emeliyyat_uslubu="MƏXARİC",
                    miqdar=float(mebleg)
                )
            elif ofis == None and shirket is not None:
                shirket_kassa = ShirketKassa.objects.get(shirket=shirket)
                if float(shirket_kassa.balans) < float(mebleg):
                    return Response({"detail": "Şirkətin kassasında yetəri qədər məbləğ yoxdur"})
                shirket_kassa.balans = float(shirket_kassa.balans) - float(mebleg)
                shirket_kassa.save()
                shirket_kassa_mexaric = ShirketKassaMexaric.objects.create(
                    mexaric_eden=user,
                    shirket_kassa=shirket_kassa,
                    mebleg=mebleg,
                    mexaric_tarixi=odeme_tarixi,
                    qeyd=qeyd
                )
                shirket_kassa_mexaric.save()

                sonraki_balans = holding_umumi_balans_hesabla()
                print(f"{sonraki_balans=}")
                shirket_sonraki_balans = shirket_balans_hesabla(shirket=shirket)
                pul_axini_create(
                    shirket=shirket,
                    aciqlama=qeyd,
                    ilkin_balans=ilkin_balans,
                    sonraki_balans=sonraki_balans,
                    shirket_ilkin_balans=shirket_ilkin_balans,
                    shirket_sonraki_balans=shirket_sonraki_balans,
                    emeliyyat_eden=user,
                    emeliyyat_uslubu="MƏXARİC",
                    miqdar=float(mebleg)
                )

            elif ofis == None and shirket == None and holding is not None:
                holding_kassa = HoldingKassa.objects.get(holding=holding)
                if float(holding_kassa.balans) < float(mebleg):
                    return Response({"detail": "Holdingin kassasında yetəri qədər məbləğ yoxdur"})
                holding_kassa.balans = float(holding_kassa.balans) - float(mebleg)
                holding_kassa.save()
                holding_kassa_mexaric = HoldingKassaMexaric.objects.create(
                    mexaric_eden=user,
                    holding_kassa=holding_kassa,
                    mebleg=mebleg,
                    mexaric_tarixi=odeme_tarixi,
                    qeyd=qeyd
                )
                holding_kassa_mexaric.save()

                sonraki_balans = holding_umumi_balans_hesabla()
                print(f"{sonraki_balans=}")
                holding_sonraki_balans = holding_balans_hesabla()
                pul_axini_create(
                    holding=holding,
                    aciqlama=qeyd,
                    ilkin_balans=ilkin_balans,
                    sonraki_balans=sonraki_balans,
                    holding_ilkin_balans=holding_ilkin_balans,
                    holding_sonraki_balans=holding_sonraki_balans,
                    emeliyyat_eden=user,
                    emeliyyat_uslubu="MƏXARİC",
                    miqdar=float(mebleg)
                )

            maas_goruntuleme.odendi = True
            maas_goruntuleme.save()
        serializer.save(mebleg=yekun_odenen_mebleg, odeme_tarixi=odeme_tarixi)
        return Response({"detail": "Maaş ödəmə yerinə yetirildi"}, status=status.HTTP_201_CREATED)

def bonus_create(self, request, *args, **kwargs):
    """
    İşçilərə bonus vermək funksiyası
    """
    serializer = self.get_serializer(data=request.data)
    user = self.request.user
    if serializer.is_valid():
        isci = serializer.validated_data.get("isci")
        mebleg = serializer.validated_data.get("mebleg")
        qeyd = serializer.validated_data.get("qeyd")
        bonus_tarixi = serializer.validated_data.get("bonus_tarixi")
        if (serializer.validated_data.get("bonus_tarixi") == None):
            bonus_tarixi = datetime.date.today()
        elif (serializer.validated_data.get("bonus_tarixi") == ""):
            bonus_tarixi = datetime.date.today()

        indi = datetime.date.today()
        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)

        maas_goruntuleme = MaasGoruntuleme.objects.get(isci=isci, tarix=next_m)
        maas_goruntuleme.yekun_maas = maas_goruntuleme.yekun_maas + float(mebleg)
        

        ofis = isci.ofis

        shirket = isci.shirket

        holding = Holding.objects.all()[0]

        qeyd = f"{user.asa} tərəfindən {isci.asa} adlı işçiyə {mebleg} AZN bonus"

        # if ofis is not None:
        #     ofis_kassa = OfisKassa.objects.get(ofis=ofis)
        #     if float(ofis_kassa.balans) < float(mebleg):
        #         return Response({"detail": "Ofisin kassasında yetəri qədər məbləğ yoxdur"})
        #     ofis_kassa.balans = float(ofis_kassa.balans) - float(mebleg)
        #     ofis_kassa.save()
        #     ofis_kassa_mexaric = OfisKassaMexaric.objects.create(
        #         mexaric_eden=user,
        #         ofis_kassa=ofis_kassa,
        #         mebleg=mebleg,
        #         mexaric_tarixi=bonus_tarixi,
        #         qeyd=qeyd
        #     )
        #     ofis_kassa_mexaric.save()
        # elif ofis == None and shirket is not None:
        #     shirket_kassa = ShirketKassa.objects.get(shirket=shirket)
        #     if float(shirket_kassa.balans) < float(mebleg):
        #         return Response({"detail": "Şirkətin kassasında yetəri qədər məbləğ yoxdur"})
        #     shirket_kassa.balans = float(shirket_kassa.balans) - float(mebleg)
        #     shirket_kassa.save()
        #     shirket_kassa_mexaric = ShirketKassaMexaric.objects.create(
        #         mexaric_eden=user,
        #         shirket_kassa=shirket_kassa,
        #         mebleg=mebleg,
        #         mexaric_tarixi=bonus_tarixi,
        #         qeyd=qeyd
        #     )
        #     shirket_kassa_mexaric.save()
        # elif ofis == None and shirket == None and holding is not None:
        #     holding_kassa = HoldingKassa.objects.get(holding=holding)
        #     if float(holding_kassa.balans) < float(mebleg):
        #         return Response({"detail": "Holdingin kassasında yetəri qədər məbləğ yoxdur"})
        #     holding_kassa.balans = float(holding_kassa.balans) - float(mebleg)
        #     holding_kassa.save()
        #     holding_kassa_mexaric = HoldingKassaMexaric.objects.create(
        #         mexaric_eden=user,
        #         holding_kassa=holding_kassa,
        #         mebleg=mebleg,
        #         mexaric_tarixi=bonus_tarixi,
        #         qeyd=qeyd
        #     )
        #     holding_kassa_mexaric.save()

        maas_goruntuleme.save()
        serializer.save(bonus_tarixi=bonus_tarixi)

        return Response({"detail": "Bonus əlavə olundu"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)

def kesinti_create(self, request, *args, **kwargs):
    """
    İşçinin maaşından kəsinti tutmaq funksiyası
    """
    serializer = self.get_serializer(data=request.data)
    user = self.request.user
    if serializer.is_valid():
        isci = serializer.validated_data.get("isci")
        mebleg = serializer.validated_data.get("mebleg")
        qeyd = serializer.validated_data.get("qeyd")
        kesinti_tarixi = serializer.validated_data.get("kesinti_tarixi")
        if (serializer.validated_data.get("kesinti_tarixi") == None):
            kesinti_tarixi = datetime.date.today()
        elif (serializer.validated_data.get("kesinti_tarixi") == ""):
            kesinti_tarixi = datetime.date.today()

        indi = datetime.date.today()
        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)

        maas_goruntuleme = MaasGoruntuleme.objects.get(isci=isci, tarix=next_m)
        maas_goruntuleme.yekun_maas = maas_goruntuleme.yekun_maas - float(mebleg)
        ofis = isci.ofis
        shirket = isci.shirket
        holding = Holding.objects.all()[0]
        qeyd = f"{user.asa} tərəfindən {isci.asa} adlı işçinin maaşından {mebleg} AZN kəsinti"

        # if ofis is not None:
        #     ofis_kassa = OfisKassa.objects.get(ofis=ofis)
        #     ofis_kassa.balans = float(ofis_kassa.balans) + float(mebleg)
        #     ofis_kassa.save()
        #     ofis_kassa_medaxil = OfisKassaMedaxil.objects.create(
        #         medaxil_eden=user,
        #         ofis_kassa=ofis_kassa,
        #         mebleg=mebleg,
        #         medaxil_tarixi=kesinti_tarixi,
        #         qeyd=qeyd
        #     )
        #     ofis_kassa_medaxil.save()
        # elif ofis == None and shirket is not None:
        #     shirket_kassa = ShirketKassa.objects.get(shirket=shirket)
        #     shirket_kassa.balans = float(shirket_kassa.balans) + float(mebleg)
        #     shirket_kassa.save()
        #     shirket_kassa_medaxil = ShirketKassaMedaxil.objects.create(
        #         medaxil_eden=user,
        #         shirket_kassa=shirket_kassa,
        #         mebleg=mebleg,
        #         medaxil_tarixi=kesinti_tarixi,
        #         qeyd=qeyd
        #     )
        #     shirket_kassa_medaxil.save()
        # elif ofis == None and shirket == None and holding is not None:
        #     holding_kassa = HoldingKassa.objects.get(holding=holding)
        #     holding_kassa.balans = float(holding_kassa.balans) + float(mebleg)
        #     holding_kassa.save()
        #     holding_kassa_medaxil = HoldingKassaMedaxil.objects.create(
        #         medaxil_eden=user,
        #         holding_kassa=holding_kassa,
        #         mebleg=mebleg,
        #         medaxil_tarixi=kesinti_tarixi,
        #         qeyd=qeyd
        #     )
        #     holding_kassa_medaxil.save()

        maas_goruntuleme.save()
        serializer.save(kesinti_tarixi=kesinti_tarixi)


        return Response({"detail": "Kəsinti əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)

def avans_create(self, request, *args, **kwargs):
    """
    İşçiyə avans vermə funksiyası
    """
    serializer = self.get_serializer(data=request.data)
    user = self.request.user
    if serializer.is_valid():
        isciler = serializer.validated_data.get("isci")
        mebleg = serializer.validated_data.get("mebleg")
        qeyd = serializer.validated_data.get("qeyd")
        avans_tarixi = serializer.validated_data.get("avans_tarixi")
        if (serializer.validated_data.get("avans_tarixi") == None):
            avans_tarixi = datetime.date.today()
        elif (serializer.validated_data.get("avans_tarixi") == ""):
            avans_tarixi = datetime.date.today()

        indi = datetime.date.today()
        d = pd.to_datetime(f"{indi.year}-{indi.month}-{1}")
        next_m = d + pd.offsets.MonthBegin(1)


        for isci in isciler:
            maas_goruntuleme = MaasGoruntuleme.objects.get(isci=isci, tarix=f"{indi.year}-{indi.month}-{1}")
            yarim_ay_emek_haqqi = serializer.validated_data.get("yarim_ay_emek_haqqi")
            if yarim_ay_emek_haqqi is not None:
                mebleg = (float(maas_goruntuleme.yekun_maas) * int(yarim_ay_emek_haqqi)) / 100

            avansdan_sonra_qalan_mebleg = maas_goruntuleme.yekun_maas - float(mebleg)

            ilkin_balans = holding_umumi_balans_hesabla()
            print(f"{ilkin_balans=}")

            if float(mebleg) > maas_goruntuleme.yekun_maas:
                return Response({"detail": "Daxil etdiyiniz məbləğ işçinin yekun maaşından daha çoxdur"}, status=status.HTTP_400_BAD_REQUEST)

            maas_goruntuleme.mebleg = mebleg
            maas_goruntuleme.yekun_maas = avansdan_sonra_qalan_mebleg

            ofis = isci.ofis
            shirket = isci.shirket
            holding = Holding.objects.all()[0]

            ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)
            shirket_ilkin_balans = shirket_balans_hesabla(shirket=shirket)
            holding_ilkin_balans = holding_balans_hesabla()

            qeyd = f"{user.asa} tərəfindən {isci.asa} adlı işçiyə {mebleg} AZN avans verildi"

            if ofis is not None:
                ofis_kassa = OfisKassa.objects.get(ofis=ofis)
                if float(ofis_kassa.balans) < float(mebleg):
                    return Response({"detail": "Ofisin kassasında yetəri qədər məbləğ yoxdur"})
                ofis_kassa.balans = float(ofis_kassa.balans) - float(mebleg)
                ofis_kassa.save()
                ofis_kassa_mexaric = OfisKassaMexaric.objects.create(
                    mexaric_eden=user,
                    ofis_kassa=ofis_kassa,
                    mebleg=mebleg,
                    mexaric_tarixi=avans_tarixi,
                    qeyd=qeyd
                )
                ofis_kassa_mexaric.save()

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
                    emeliyyat_uslubu="MƏXARİC",
                    miqdar=float(mebleg)
                )
            elif ofis == None and shirket is not None:
                shirket_kassa = ShirketKassa.objects.get(shirket=shirket)
                if float(shirket_kassa.balans) < float(mebleg):
                    return Response({"detail": "Şirkətin kassasında yetəri qədər məbləğ yoxdur"})
                shirket_kassa.balans = float(shirket_kassa.balans) - float(mebleg)
                shirket_kassa.save()
                shirket_kassa_mexaric = ShirketKassaMexaric.objects.create(
                    mexaric_eden=user,
                    shirket_kassa=shirket_kassa,
                    mebleg=mebleg,
                    mexaric_tarixi=avans_tarixi,
                    qeyd=qeyd
                )
                shirket_kassa_mexaric.save()

                sonraki_balans = holding_umumi_balans_hesabla()
                print(f"{sonraki_balans=}")
                shirket_sonraki_balans = shirket_balans_hesabla(shirket=shirket)
                pul_axini_create(
                    shirket=shirket,
                    aciqlama=qeyd,
                    ilkin_balans=ilkin_balans,
                    sonraki_balans=sonraki_balans,
                    shirket_ilkin_balans=shirket_ilkin_balans,
                    shirket_sonraki_balans=shirket_sonraki_balans,
                    emeliyyat_eden=user,
                    emeliyyat_uslubu="MƏXARİC",
                    miqdar=float(mebleg)
                )

            elif ofis == None and shirket == None and holding is not None:
                holding_kassa = HoldingKassa.objects.get(holding=holding)
                if float(holding_kassa.balans) < float(mebleg):
                    return Response({"detail": "Holdingin kassasında yetəri qədər məbləğ yoxdur"})
                holding_kassa.balans = float(holding_kassa.balans) - float(mebleg)
                holding_kassa.save()
                holding_kassa_mexaric = HoldingKassaMexaric.objects.create(
                    mexaric_eden=user,
                    holding_kassa=holding_kassa,
                    mebleg=mebleg,
                    mexaric_tarixi=avans_tarixi,
                    qeyd=qeyd
                )
                holding_kassa_mexaric.save()

                sonraki_balans = holding_umumi_balans_hesabla()
                print(f"{sonraki_balans=}")
                holding_sonraki_balans = holding_balans_hesabla()
                pul_axini_create(
                    holding=holding,
                    aciqlama=qeyd,
                    ilkin_balans=ilkin_balans,
                    sonraki_balans=sonraki_balans,
                    holding_ilkin_balans=holding_ilkin_balans,
                    holding_sonraki_balans=holding_sonraki_balans,
                    emeliyyat_eden=user,
                    emeliyyat_uslubu="MƏXARİC",
                    miqdar=float(mebleg)
                )

            maas_goruntuleme.save()
        serializer.save(mebleg=mebleg, avans_tarixi=avans_tarixi)
        return Response({"detail": "Avans vermə əməliyyatı yerinə yetirildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Xəta baş verdi"}, status=status.HTTP_400_BAD_REQUEST)