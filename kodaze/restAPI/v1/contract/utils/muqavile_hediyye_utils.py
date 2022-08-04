from rest_framework import status

from rest_framework.response import Response
from cashbox.models import OfisKassa

from warehouse.models import (
    Anbar,
    Stok
)

from restAPI.v1.contract.utils.muqavile_utils import (
    stok_mehsul_ciximi, 
    stok_mehsul_elave, 
    k_medaxil, 
    k_mexaric
)
from rest_framework.generics import get_object_or_404


def muqavile_hediyye_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    user = request.user

    if serializer.is_valid():
        mehsullar = serializer.validated_data.get("mehsul")
        muqavile = serializer.validated_data.get("muqavile")
        vanleader = muqavile.vanleader
        say = serializer.validated_data.get("say")
        if say == None or say == "":
            say = 1

        if muqavile.ofis == None:
            ofis = serializer.validated_data.get("ofis")
            if ofis == None or ofis == "":
                return Response({"detail": "Ofis daxil edin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            ofis = muqavile.ofis

        try:
            anbar = get_object_or_404(Anbar, ofis=ofis)
        except:
            return Response({"detail": "Anbar tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)

        for mehsul in mehsullar:
            try:
                stok = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)
                stok_mehsul_ciximi(stok, say)
            except:
                return Response({"detail": "Stokda məhsul qalmayıb"}, status=status.HTTP_404_NOT_FOUND)

            if mehsul.qiymet > 0:
                try:
                    kassa = OfisKassa.objects.filter(ofis=ofis)[0]
                except:
                    return Response({"detail": "Ofis Kassa tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)
                daxil_edilecek_mebleg = float(mehsul.qiymet)*int(say)
                qeyd = f"{muqavile} müqviləsinə {user.asa} tərəfindən {say} ədəd {mehsul} hədiyyə verildiyi üçün, {kassa} ofis kassasına {daxil_edilecek_mebleg} AZN mədaxil edildi"
                k_medaxil(
                    company_kassa=kassa,
                    daxil_edilecek_mebleg=daxil_edilecek_mebleg,
                    vanleader=user,
                    qeyd=qeyd
                )

        serializer.save(ofis=ofis)
        return Response({"detail": f"{muqavile} müqaviləsinə hədiyyə verildi"}, status=status.HTTP_200_OK)


def muqavile_hediyye_destroy(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    muqavile_hediyye = self.get_object()
    user = request.user

    mehsul_query_set = muqavile_hediyye.mehsul.all()
    mehsullar = list(mehsul_query_set)
    muqavile = muqavile_hediyye.muqavile
    vanleader = muqavile.vanleader
    anbar = get_object_or_404(Anbar, ofis=muqavile.ofis)
    say = muqavile_hediyye.say
    for mehsul in mehsullar:
        ofis = muqavile.ofis
        if mehsul.qiymet > 0:
            try:
                kassa = OfisKassa.objects.filter(ofis=ofis)[0]
            except:
                return Response({"detail": "Ofis Kassa tapılmadı"}, status=status.HTTP_400_BAD_REQUEST)
            daxil_edilecek_mebleg = float(mehsul.qiymet)*int(say)
            if daxil_edilecek_mebleg > float(kassa.balans):
                return Response({"detail": "Kassanın balansında yetəri qədər məbləğ yoxdur"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                qeyd = f"{muqavile} müqviləsindən {user.asa} tərəfindən {say} ədəd {mehsul} hədiyyəsi geri alındığı üçün, {kassa} ofis kassasından {daxil_edilecek_mebleg} AZN məxaric edildi"
                k_mexaric(
                    company_kassa=kassa,
                    daxil_edilecek_mebleg=daxil_edilecek_mebleg,
                    vanleader=user,
                    qeyd=qeyd
                )
        try:
            stok = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)
            stok_mehsul_elave(stok, say)
        except:
            stok = Stok.objects.create(anbar=anbar, mehsul=mehsul, say=say)
            stok.save()
        
    muqavile_hediyye.delete()
    return Response({"detail": "Hədiyyə stok-a geri qaytarıldı"}, status=status.HTTP_200_OK)
