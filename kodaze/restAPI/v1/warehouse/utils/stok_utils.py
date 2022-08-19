import datetime
from rest_framework import status
from rest_framework.response import Response
from warehouse.models import Emeliyyat


def stok_update(self, request, *args, **kwargs):
    stok = self.get_object()
    serializer = self.get_serializer(stok, data=request.data, partial=True)
    mehsul = stok.mehsul
    tarix = datetime.date.today()
    say = int(request.data.get("say"))
    if say==0:
        return Response({"detail": "Say 0 ola bilməz"}, status=status.HTTP_400_BAD_REQUEST)
    icraci = request.user
    evvelki_say = stok.say
    yekun_say = abs(int(evvelki_say) - int(say))
    print(f"{say=}")
    print(f"{evvelki_say=}")
    print(f"{yekun_say=}")
    if serializer.is_valid():
        qeyd = serializer.validated_data.get("qeyd")
        serializer.save(say=say)
        emeliyyat = Emeliyyat.objects.create(
                icraci=icraci,
                say=yekun_say,
                emeliyyat_novu="stok yeniləmə",
                emeliyyat_tarixi=tarix,
                qeyd=qeyd,
                gonderen=None,
                qebul_eden=None,
                mehsul_ve_sayi=mehsul.mehsulun_adi
            )
        emeliyyat.save()
        return Response({"detail": "Məlumatlar yeniləndi"}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Xəta baş verdi!"}, status=status.HTTP_400_BAD_REQUEST)
    # try:
    #     # stok = get_object_or_404(Stok, anbar=anbar, mehsul=mehsul)

    #     stok.say = stok.say + say
    #     stok.save()
    #     # super(StokSerializer, self).update(request, *args, **kwargs)
    #     return Response({"detail" : "Məlumatlar yeniləndi"}, status=status.HTTP_200_OK)
    # except:
    #     return Response({"detail" : "Problem"}, status=status.HTTP_400_BAD_REQUEST)
