import traceback
from rest_framework import status
from rest_framework.response import Response

from product.models import (
    Mehsullar,
)
from warehouse.models import Stok
from rest_framework.generics import get_object_or_404


def emeliyyat_create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
        try:
            icraci = request.user
            gonderen = serializer.validated_data.get("gonderen")
            qebul_eden = serializer.validated_data.get("qebul_eden")

            if gonderen.shirket != qebul_eden.shirket:
                return Response({"detail": "Əməliyyat yalnız eyni şirkətin anbarları arasında ola bilər"}, status=status.HTTP_404_NOT_FOUND)

            mehsul_ve_sayi = serializer.validated_data.get("mehsul_ve_sayi")
            mehsul_ve_sayi_list = mehsul_ve_sayi.split(",")
            for m in mehsul_ve_sayi_list:
                mehsul_ve_say = m.split("-")
                mehsul_id = int(mehsul_ve_say[0].strip())
                say = int(mehsul_ve_say[1])
                mehsul = Mehsullar.objects.get(pk=mehsul_id)
                try:
                    stok1 = get_object_or_404(
                        Stok, anbar=gonderen, mehsul=mehsul)
                except:
                    return Response({"detail": "Göndərən anbarda məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)
                if stok1 == None:
                    return Response({"detail": "Göndərən anbarda məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)
                if (say > stok1.say):
                    return Response({"detail": "Göndərən anbarda yetəri qədər məhsul yoxdur"}, status=status.HTTP_404_NOT_FOUND)
                try:
                    stok2 = get_object_or_404(
                        Stok, anbar=qebul_eden, mehsul=mehsul)
                    if (stok1 == stok2):
                        return Response({"detail": "Göndərən və göndərilən anbar eynidir!"}, status=status.HTTP_404_NOT_FOUND)
                    stok1.say = stok1.say - say
                    stok1.save()
                    if (stok1.say == 0):
                        stok1.delete()
                    stok2.say = stok2.say + say
                    stok2.save()
                    if (serializer.is_valid()):
                        serializer.save(
                            icraci=icraci, gonderen=gonderen, say=None, emeliyyat_novu="transfer")
                except:
                    stok2 = Stok.objects.create(
                        anbar=qebul_eden, mehsul=mehsul, say=say)
                    if (stok1 == stok2):
                        return Response({"detail": "Göndərən və göndərilən anbar eynidir!"}, status=status.HTTP_404_NOT_FOUND)
                    stok2.save()
                    stok1.say = stok1.say - say
                    stok1.save()
                    if (serializer.is_valid()):
                        serializer.save(
                            icraci=icraci, gonderen=gonderen, say=None, emeliyyat_novu="transfer")
        except:
            traceback.print_exc()
        return Response({"detail": "Əməliyyat uğurla yerinə yetirildi"}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Məlumatları doğru daxil edin"}, status=status.HTTP_404_NOT_FOUND)
