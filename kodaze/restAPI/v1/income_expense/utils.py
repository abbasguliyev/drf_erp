from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from company.models import Holding
from cashbox.models import HoldingKassa, OfisKassa, ShirketKassa

from restAPI.v1.cashbox.utils import holding_umumi_balans_hesabla, pul_axini_create, shirket_balans_hesabla, ofis_balans_hesabla, holding_balans_hesabla


# *************** Holding Kassa medaxil mexaric ***************
def holding_kassa_medaxil_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    mebleg = request.data.get("mebleg")
    user = request.user

    if(mebleg != None):
        holding = get_object_or_404(Holding, holding_adi="ALLIANCE")
        holding_kassa = get_object_or_404(HoldingKassa, holding=holding)
        evvelki_balans=holding_kassa.balans

        ilkin_balans = holding_umumi_balans_hesabla()
        print(f"{ilkin_balans=}")
        holding_ilkin_balans = holding_balans_hesabla()

        medaxil_tarixi = request.data.get("medaxil_tarixi")

        if(medaxil_tarixi == None):
            medaxil_tarixi = datetime.today().strftime('%Y-%m-%d')

        qeyd = request.data.get("qeyd")

        holding_kassa_balans = holding_kassa.balans

        yekun_balans = float(mebleg) + float(holding_kassa_balans)

        if(serializer.is_valid()):
            holding_kassa.balans = yekun_balans
            holding_kassa.save()

            sonraki_kassa_balans=holding_kassa.balans

            serializer.save(medaxil_eden=user, holding_kassa=holding_kassa, medaxil_tarixi=medaxil_tarixi, evvelki_balans=evvelki_balans, sonraki_balans=sonraki_kassa_balans)

            sonraki_balans = holding_umumi_balans_hesabla()
            print(f"{sonraki_balans=}")
            holding_sonraki_balans = holding_balans_hesabla()

            pul_axini_create(
                holding=holding,
                emeliyyat_uslubu="MƏDAXİL",
                aciqlama=f"{holding.holding_adi} holdinq kassasına {float(mebleg)} AZN mədaxil edildi",
                ilkin_balans=ilkin_balans,
                sonraki_balans=sonraki_balans,
                holding_ilkin_balans=holding_ilkin_balans,
                holding_sonraki_balans=holding_sonraki_balans,
                emeliyyat_eden=user,
                tarix=medaxil_tarixi,
                miqdar=float(mebleg)
            )

            return Response({"detail": f"{holding} holdinqinə {mebleg} azn mədaxil edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məbləği daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

def holding_kassa_mexaric_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    mebleg = request.data.get("mebleg")

    user = request.user

    qeyd = request.data.get("qeyd")

    holding = get_object_or_404(Holding, holding_adi="ALLIANCE")
    holding_kassa = get_object_or_404(HoldingKassa, holding=holding)
    evvelki_balans=holding_kassa.balans

    ilkin_balans = holding_umumi_balans_hesabla()
    print(f"{ilkin_balans=}")
    holding_ilkin_balans = holding_balans_hesabla()

    holding_kassa_balans = holding_kassa.balans

    mexaric_tarixi = request.data.get("mexaric_tarixi")

    if(mexaric_tarixi == None):
        mexaric_tarixi = datetime.today().strftime('%Y-%m-%d')

    if(holding_kassa_balans != 0):
        if(mebleg != None):
            if(float(mebleg) <= float(holding_kassa_balans)):
                yekun_balans = float(holding_kassa_balans) - float(mebleg)
                if(serializer.is_valid()):
                    holding_kassa.balans = yekun_balans
                    holding_kassa.save()
                    
                    sonraki_kassa_balans=holding_kassa.balans

                    serializer.save(mexaric_eden=user, holding_kassa=holding_kassa, mexaric_tarixi=mexaric_tarixi, evvelki_balans=evvelki_balans, sonraki_balans=sonraki_kassa_balans)

                    sonraki_balans = holding_umumi_balans_hesabla()
                    print(f"{sonraki_balans=}")
                    holding_sonraki_balans = holding_balans_hesabla()

                    pul_axini_create(
                        holding=holding,
                        emeliyyat_uslubu="MƏXARİC",
                        aciqlama=f"{holding.holding_adi} holdinq kassasından {float(mebleg)} AZN məxaric edildi",
                        ilkin_balans=ilkin_balans,
                        sonraki_balans=sonraki_balans,
                        holding_ilkin_balans=holding_ilkin_balans,
                        holding_sonraki_balans=holding_sonraki_balans,
                        emeliyyat_eden=user,
                        tarix=mexaric_tarixi,
                        miqdar=float(mebleg)
                    )

                    return Response({"detail": f"{holding} holdinqindən {mebleg} azn məxaric edildi"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Daxil etdiyiniz məbləğ holdinqin balansıdan böyük ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Holdinqin balansı 0-dır"}, status=status.HTTP_400_BAD_REQUEST)

# *************** Shirket Kassa medaxil mexaric ***************

def shirket_kassa_medaxil_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    mebleg = request.data.get("mebleg")
    user = request.user
    
    if(mebleg != ""):
        shirket_kassa_id = request.data.get("shirket_kassa_id")
        shirket_kassa = get_object_or_404(ShirketKassa, pk=shirket_kassa_id)

        evvelki_balans=shirket_kassa.balans

        shirket=shirket_kassa.shirket

        medaxil_tarixi = request.data.get("medaxil_tarixi")

        ilkin_balans = holding_umumi_balans_hesabla()
        print(f"{ilkin_balans=}")

        shirket_ilkin_balans = shirket_balans_hesabla(shirket=shirket)

        if(medaxil_tarixi == ""):
            medaxil_tarixi = datetime.today().strftime('%Y-%m-%d')

        qeyd = request.data.get("qeyd")

        shirket_kassa_balans = shirket_kassa.balans

        yekun_balans = float(mebleg) + float(shirket_kassa_balans)

        if(serializer.is_valid()):
            shirket_kassa.balans = yekun_balans
            shirket_kassa.save()

            sonraki_kassa_balans=shirket_kassa.balans

            serializer.save(medaxil_eden=user, shirket_kassa=shirket_kassa, medaxil_tarixi=medaxil_tarixi, evvelki_balans=evvelki_balans, sonraki_balans=sonraki_kassa_balans)

            sonraki_balans = holding_umumi_balans_hesabla()
            print(f"{sonraki_balans=}")
            shirket_sonraki_balans = shirket_balans_hesabla(shirket=shirket)
            pul_axini_create(
                shirket=shirket,
                emeliyyat_uslubu="MƏDAXİL",
                aciqlama=f"{shirket.shirket_adi} şirkət kassasına {float(mebleg)} AZN mədaxil edildi",
                ilkin_balans=ilkin_balans,
                sonraki_balans=sonraki_balans,
                shirket_ilkin_balans=shirket_ilkin_balans,
                shirket_sonraki_balans=shirket_sonraki_balans,
                emeliyyat_eden=user,
                tarix=medaxil_tarixi,
                miqdar=float(mebleg)
            )

            return Response({"detail": f"{shirket_kassa.shirket} şirkətinə {mebleg} azn mədaxil edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məbləği daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

def shirket_kassa_mexaric_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    mebleg = request.data.get("mebleg")

    user = request.user

    qeyd = request.data.get("qeyd")

    shirket_kassa_id = request.data.get("shirket_kassa_id")
    shirket_kassa = get_object_or_404(ShirketKassa, pk=shirket_kassa_id)
    shirket=shirket_kassa.shirket

    evvelki_balans=shirket_kassa.balans

    ilkin_balans = holding_umumi_balans_hesabla()
    print(f"{ilkin_balans=}")
    shirket_ilkin_balans = shirket_balans_hesabla(shirket=shirket)

    shirket_kassa_balans = shirket_kassa.balans

    mexaric_tarixi = request.data.get("mexaric_tarixi")

    if(mexaric_tarixi == ""):
        mexaric_tarixi = datetime.today().strftime('%Y-%m-%d')

    if(shirket_kassa_balans != 0):
        if(mebleg != ""):
            if(float(mebleg) <= float(shirket_kassa_balans)):
                yekun_balans = float(shirket_kassa_balans) - float(mebleg)
                if(serializer.is_valid()):
                    shirket_kassa.balans = yekun_balans
                    shirket_kassa.save()
                    
                    sonraki_kassa_balans=shirket_kassa.balans

                    serializer.save(mexaric_eden=user, shirket_kassa=shirket_kassa, mexaric_tarixi=mexaric_tarixi, evvelki_balans=evvelki_balans, sonraki_balans=sonraki_kassa_balans)

                    sonraki_balans = holding_umumi_balans_hesabla()
                    print(f"{sonraki_balans=}")
                    shirket_sonraki_balans = shirket_balans_hesabla(shirket=shirket)
                    pul_axini_create(
                        shirket=shirket,
                        emeliyyat_uslubu="MƏXARİC",
                        aciqlama=f"{shirket.shirket_adi} şirkət kassasından {float(mebleg)} AZN məxaric edildi",
                        ilkin_balans=ilkin_balans,
                        sonraki_balans=sonraki_balans,
                        shirket_ilkin_balans=shirket_ilkin_balans,
                        shirket_sonraki_balans=shirket_sonraki_balans,
                        emeliyyat_eden=user,
                        tarix=mexaric_tarixi,
                        miqdar=float(mebleg)
                    )
                    return Response({"detail": f"{shirket_kassa.shirket} şirkətindən {mebleg} azn məxaric edildi"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Daxil etdiyiniz məbləğ şirkətinin balansıdan böyük ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Şirkətin balansı 0-dır"}, status=status.HTTP_400_BAD_REQUEST)

# *************** Ofis Kassa medaxil mexaric ***************

def ofis_kassa_medaxil_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    mebleg = request.data.get("mebleg")
    user = request.user

    if(mebleg != ""):
        ofis_kassa_id = request.data.get("ofis_kassa_id")
        ofis_kassa = get_object_or_404(OfisKassa, pk=ofis_kassa_id)
        medaxil_tarixi = request.data.get("medaxil_tarixi")
        ofis=ofis_kassa.ofis
        evvelki_balans=ofis_kassa.balans

        ilkin_balans = holding_umumi_balans_hesabla()
        print(f"{ilkin_balans=}")
        ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)
        if(medaxil_tarixi == ""):
            medaxil_tarixi = datetime.today().strftime('%Y-%m-%d')
        qeyd = request.data.get("qeyd")
        ofis_kassa_balans = ofis_kassa.balans
        yekun_balans = float(mebleg) + float(ofis_kassa_balans)

        if(serializer.is_valid()):
            ofis_kassa.balans = yekun_balans
            ofis_kassa.save()
            sonraki_kassa_balans=ofis_kassa.balans
            serializer.save(medaxil_eden=user, ofis_kassa=ofis_kassa, medaxil_tarixi=medaxil_tarixi, evvelki_balans=evvelki_balans, sonraki_balans=sonraki_kassa_balans)
            sonraki_balans = holding_umumi_balans_hesabla()
            print(f"{sonraki_balans=}")
            ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
            pul_axini_create(
                ofis=ofis,
                shirket=ofis.shirket,
                emeliyyat_uslubu="MƏDAXİL",
                aciqlama=f"{ofis.ofis_adi} ofis kassasına {float(mebleg)} AZN əlavə edildi",
                ilkin_balans=ilkin_balans,
                sonraki_balans=sonraki_balans,
                ofis_ilkin_balans=ofis_ilkin_balans,
                ofis_sonraki_balans=ofis_sonraki_balans,
                emeliyyat_eden=user,
                tarix=medaxil_tarixi,
                miqdar=float(mebleg)
            )
            return Response({"detail": f"{ofis_kassa.ofis} ofisinə {mebleg} azn mədaxil edildi"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Məbləği daxil edin"}, status=status.HTTP_400_BAD_REQUEST)

def ofis_kassa_mexaric_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    mebleg = request.data.get("mebleg")
    qeyd = request.data.get("qeyd")
    user = request.user

    ofis_kassa_id = request.data.get("ofis_kassa_id")
    ofis_kassa = get_object_or_404(OfisKassa, pk=ofis_kassa_id)
    ofis=ofis_kassa.ofis
    evvelki_balans=ofis_kassa.balans

    ilkin_balans = holding_umumi_balans_hesabla()
    print(f"{ilkin_balans=}")

    ofis_ilkin_balans = ofis_balans_hesabla(ofis=ofis)

    ofis_kassa_balans = ofis_kassa.balans
    mexaric_tarixi = request.data.get("mexaric_tarixi")
    if(mexaric_tarixi == ""):
        mexaric_tarixi = datetime.today().strftime('%Y-%m-%d')

    if(ofis_kassa_balans != 0):
        if(mebleg != ""):
            if(float(mebleg) <= float(ofis_kassa_balans)):
                yekun_balans = float(ofis_kassa_balans) - float(mebleg)
                if(serializer.is_valid()):
                    ofis_kassa.balans = yekun_balans
                    ofis_kassa.save()
                    sonraki_kassa_balans=ofis_kassa.balans
                    serializer.save(mexaric_eden=user, ofis_kassa=ofis_kassa, mexaric_tarixi=mexaric_tarixi, evvelki_balans=evvelki_balans, sonraki_balans=sonraki_kassa_balans)
                    sonraki_balans = holding_umumi_balans_hesabla()
                    print(f"{sonraki_balans=}")
                    ofis_sonraki_balans = ofis_balans_hesabla(ofis=ofis)
                    pul_axini_create(
                        ofis=ofis,
                        shirket=ofis.shirket,
                        emeliyyat_uslubu="MƏXARİC",
                        aciqlama=f"{ofis.ofis_adi} ofis kassasından {float(mebleg)} AZN məxaric edildi",
                        ilkin_balans=ilkin_balans,
                        sonraki_balans=sonraki_balans,
                        ofis_ilkin_balans=ofis_ilkin_balans,
                        ofis_sonraki_balans=ofis_sonraki_balans,
                        emeliyyat_eden=user,
                        tarix=mexaric_tarixi,
                        miqdar=float(mebleg)
                    )
                    return Response({"detail": f"{ofis_kassa.ofis} ofisindən {mebleg} azn məxaric edildi"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Daxil etdiyiniz məbləğ ofisin balansıdan böyük ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Məbləği doğru daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Ofisin balansı 0-dır"}, status=status.HTTP_400_BAD_REQUEST)